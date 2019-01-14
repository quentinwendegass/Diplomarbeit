//
//  WebRTCClient.swift
//  SIMplePhoneKit
//
//  Created by Lukas Kuster on 25.11.18.
//  Copyright © 2018 Lukas Kuster. All rights reserved.
//

import Foundation
import WebRTC
import AVFoundation

public protocol WebRTCClientDelegate {
    func webRTCClient(client: WebRTCClient, didReceiveError error: Error)
    func webRTCClient(client: WebRTCClient, didReceiveRemoteTrack track: RTCAudioTrack)
}

public class WebRTCClient: NSObject {
    public static let shared = WebRTCClient()
    public var delegate: WebRTCClientDelegate?
    private var connectionFactory: RTCPeerConnectionFactory
    private var peerConnection: RTCPeerConnection
    
    private var iceCandidatesAvailable: Bool = false
    
    private override init() {
        RTCPeerConnectionFactory.initialize()
        self.connectionFactory = RTCPeerConnectionFactory()

        let configuration = RTCConfiguration()
        configuration.iceServers = [RTCIceServer(urlStrings: ["stun:stun.l.google.com:19302",
                                                              "stun:stun1.l.google.com:19302",
                                                              "stun:stun2.l.google.com:19302",
                                                              "stun:stun3.l.google.com:19302",
                                                              "stun:stun4.l.google.com:19302"])]
        let constraint = RTCMediaConstraints(mandatoryConstraints: nil, optionalConstraints: ["DtlsSrtpKeyAgreement": "true"])
        self.peerConnection = self.connectionFactory.peerConnection(with: configuration, constraints: constraint, delegate: nil)
//        self.peerConnection.stopRtcEventLog()
        super.init()
        self.peerConnection.delegate = self
    }
    
    func setupSdp() {
        RTCPeerConnectionFactory.initialize()
        self.connectionFactory = RTCPeerConnectionFactory()
        
        let configuration = RTCConfiguration()
        configuration.iceServers = [RTCIceServer(urlStrings: ["stun:stun.l.google.com:19302",
                                                              "stun:stun1.l.google.com:19302",
                                                              "stun:stun2.l.google.com:19302",
                                                              "stun:stun3.l.google.com:19302",
                                                              "stun:stun4.l.google.com:19302"])]
        let constraint = RTCMediaConstraints(mandatoryConstraints: nil, optionalConstraints: ["DtlsSrtpKeyAgreement": "true"])
        self.peerConnection = self.connectionFactory.peerConnection(with: configuration, constraints: constraint, delegate: nil)
        self.peerConnection.delegate = self
    }
    
    func addMicrophone() -> RTCMediaStream {
        let stream = self.connectionFactory.mediaStream(withStreamId: "RTCmS")
        if !AVCaptureState.isAudioDisabled {
            let track = self.connectionFactory.audioTrack(withTrackId: "RTCaS0")
            stream.addAudioTrack(track)
        }else{
            let error = NSError(domain: "audioPermissionDenied", code: 0, userInfo: nil)
            self.delegate?.webRTCClient(client: self, didReceiveError: error)
        }
        return stream
    }
    
    func generateOffer(completion: @escaping (_ success: Bool, _ sdp: String?, _ error: Error?) -> Void) {
        print("current gathering state: \(self.peerConnection.iceGatheringState.rawValue)")
        let constraint = RTCMediaConstraints(mandatoryConstraints: ["OfferToReceiveAudio": "true"], optionalConstraints: nil)
        self.peerConnection.offer(for: constraint) { (sdp, error) in
            print("gathering now?")
            print("current gathering state: \(self.peerConnection.iceGatheringState.rawValue)")
            if let error = error {
                self.delegate?.webRTCClient(client: self, didReceiveError: error)
            }else{
                self.peerConnection.setLocalDescription(self.pcmaOnlySdp(sdp!), completionHandler: { (error) in
                    print("gathering now?")
                    print("current gathering state: \(self.peerConnection.iceGatheringState.rawValue)")
                    
                    
                    if let error = error {
                        completion(false, nil, error)
                    }else{
                        if let localDescription = self.peerConnection.localDescription {
                            completion(true, localDescription.sdp, nil)
                        }else{
                            completion(false, nil, error!)
                        }
                        
                    }
                })
                
            }
        }
    }
    
    func handle(offer offerSdp: String, completion: @escaping (_ success: Bool, _ answer: String?, _ error: Error?) -> Void) {
        let sdp = RTCSessionDescription(type: .offer, sdp: offerSdp)
        self.peerConnection.setRemoteDescription(sdp) { (error) in
            if let error = error {
                completion(false, nil, error)
            }else{
                let constraint = RTCMediaConstraints(mandatoryConstraints: ["OfferToReceiveAudio": "true"], optionalConstraints: nil)
                self.peerConnection.answer(for: constraint, completionHandler: { (sdp, error) in
                    if let error = error {
                        completion(false, nil, error)
                    }else{
                        completion(true, sdp!.sdp, nil)
                    }
                })
            }
        }
    }
    
    func handle(answer answerSdp: String, completion: @escaping (_ success: Bool, _ error: Error?) -> Void) {
        let sdp = RTCSessionDescription(type: .answer, sdp: answerSdp)
        self.peerConnection.setRemoteDescription(sdp) { (error) in
            if let error = error {
                completion(false, error)
            }else{
                completion(true, nil)
            }
        }
    }
    
    func startConnection() {
        self.setupSdp()
        let localStream = self.addMicrophone()
        self.peerConnection.add(localStream)
    }
    
    func closeConnection() {
        if let stream = self.peerConnection.localStreams.first {
            self.peerConnection.remove(stream)
        }
        self.peerConnection.close()
    }
    
}

extension WebRTCClient {
    /*
     Workaround for missing RTCRtpTransceiver.setCodecPreferences() in WebRTC.framework
     */
    private func pcmaOnlySdp(_ sdp: RTCSessionDescription) -> RTCSessionDescription {
        let regex = try! NSRegularExpression(pattern: "a=rtpmap:(?!8 PCMA)(.*)\n", options: NSRegularExpression.Options.caseInsensitive)
        let range = NSMakeRange(0, sdp.sdp.count)
        let modSdp = regex.stringByReplacingMatches(in: sdp.sdp, options: [], range: range, withTemplate: "")
        return RTCSessionDescription(type: sdp.type, sdp: modSdp)
    }
}

extension WebRTCClient: RTCPeerConnectionDelegate {
    public func peerConnection(_ peerConnection: RTCPeerConnection, didChange stateChanged: RTCSignalingState) {
        print("peerConnection: didChange RTCSignalingState")
        debugPrint(stateChanged)
    }
    
    public func peerConnection(_ peerConnection: RTCPeerConnection, didAdd stream: RTCMediaStream) {
        print("peerConnection: didAdd RTCMediaStream")
        debugPrint(stream)
        
        if stream.audioTracks.count > 0 {
            self.delegate?.webRTCClient(client: self, didReceiveRemoteTrack: stream.audioTracks.first!)
        }
    }
    
    public func peerConnection(_ peerConnection: RTCPeerConnection, didRemove stream: RTCMediaStream) {
        print("peerConnection: didRemove RTCMediaStream")
        debugPrint(stream)
    }
    
    public func peerConnection(_ peerConnection: RTCPeerConnection, didChange newState: RTCIceConnectionState) {
        print("peerConnection: didChange RTCIceConnectionState")
        debugPrint(newState)
    }
    
    public func peerConnection(_ peerConnection: RTCPeerConnection, didChange newState: RTCIceGatheringState) {
        print("peerConnection: didChange RTCIceGatheringState")
        print("\(newState.rawValue)")
        if case .complete = newState {
            print("completed getting candidates")
            self.iceCandidatesAvailable = true
        }
    }
    
    public func peerConnection(_ peerConnection: RTCPeerConnection, didGenerate candidate: RTCIceCandidate) {
        SignalingClient.shared.postCandidate(candidate: candidate.sdp) { (success, error) in
            print("post candidate \(candidate)")
            if !success {
                print("Error: RTCIceCandidate/Signalling \(error)")
            }
        }
        print("peerConnection: didGenerate RTCIceCandidate")
        debugPrint(candidate)
    }
    
    public func peerConnection(_ peerConnection: RTCPeerConnection, didRemove candidates: [RTCIceCandidate]) {
        print("peerConnection: didRemove RTCIceCandidate")
        debugPrint(candidates)
    }
    
    public func peerConnection(_ peerConnection: RTCPeerConnection, didOpen dataChannel: RTCDataChannel) {
        print("peerConnection: didOpen RTCDataChannel")
        debugPrint(dataChannel)
    }
    
    public func peerConnectionShouldNegotiate(_ peerConnection: RTCPeerConnection) {
        print("peerConnection: ShouldNegotiate RTCPeerConnection")
        debugPrint(peerConnection)
    }
}
