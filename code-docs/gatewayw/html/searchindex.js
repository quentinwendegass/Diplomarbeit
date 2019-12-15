Search.setIndex({docnames:["gateway","gateway.core","gateway.io","gateway.io.pcm","gateway.io.sim800","gateway.networking","gateway.utils","index","pcmlib"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.viewcode":1,sphinx:55},filenames:["gateway.rst","gateway.core.rst","gateway.io.rst","gateway.io.pcm.rst","gateway.io.sim800.rst","gateway.networking.rst","gateway.utils.rst","index.rst","pcmlib.rst"],objects:{"gateway.core":{config:[1,0,0,"-"],main:[1,0,0,"-"]},"gateway.core.config":{get_apn_config_path:[1,1,1,""],get_config:[1,1,1,""],set_config:[1,1,1,""]},"gateway.core.main":{check_imei:[1,1,1,""],check_pin_status:[1,1,1,""],main:[1,1,1,""],on_answer_call:[1,1,1,""],on_connection_closed:[1,1,1,""],on_dial:[1,1,1,""],on_enter_pin:[1,1,1,""],on_hang_up:[1,1,1,""],on_hold_call:[1,1,1,""],on_outgoing_call:[1,1,1,""],on_play_dtmf:[1,1,1,""],on_request_signal:[1,1,1,""],on_resume_call:[1,1,1,""],on_send_sms:[1,1,1,""],on_signaling_timeout:[1,1,1,""],start:[1,1,1,""]},"gateway.io.pcm":{pcm:[3,0,0,"-"],register_control:[3,0,0,"-"]},"gateway.io.pcm.pcm":{PCM:[3,2,1,""]},"gateway.io.pcm.pcm.PCM":{disable:[3,3,1,""],enable:[3,3,1,""],read_frame:[3,3,1,""],write_frame:[3,3,1,""]},"gateway.io.pcm.register_control":{ModeControlRegister:[3,2,1,""],Register:[3,2,1,""],address:[3,1,1,""],null_bits:[3,1,1,""]},"gateway.io.pcm.register_control.ModeControlRegister":{ALB:[3,4,1,""],COMPANDING:[3,4,1,""],CPB:[3,4,1,""],DLB:[3,4,1,""],PD:[3,4,1,""],TXZ:[3,4,1,""],address:[3,4,1,""]},"gateway.io.pcm.register_control.Register":{read:[3,3,1,""],write:[3,3,1,""]},"gateway.io.sim800":{at_command:[4,0,0,"-"],at_event:[4,0,0,"-"],at_parser:[4,0,0,"-"],at_response:[4,0,0,"-"],serial_loop:[4,0,0,"-"],sim800:[4,0,0,"-"]},"gateway.io.sim800.at_command":{ATCommand:[4,2,1,""]},"gateway.io.sim800.at_event":{ATEvent:[4,2,1,""]},"gateway.io.sim800.at_event.ATEvent":{clear:[4,3,1,""],set:[4,3,1,""]},"gateway.io.sim800.at_parser":{ATParser:[4,2,1,""],CallerIdentificationParser:[4,2,1,""],IMEIParser:[4,2,1,""],IMSIParser:[4,2,1,""],NetworkStatusParser:[4,2,1,""],ParseError:[4,6,1,""],PinStatusParser:[4,2,1,""],SMSListParser:[4,2,1,""],SignalQualityParser:[4,2,1,""],SubscriberNumberParser:[4,2,1,""]},"gateway.io.sim800.at_parser.ATParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_parser.CallerIdentificationParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_parser.IMEIParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_parser.IMSIParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_parser.NetworkStatusParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_parser.PinStatusParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_parser.SMSListParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_parser.SignalQualityParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_parser.SubscriberNumberParser":{parse:[4,5,1,""]},"gateway.io.sim800.at_response":{ATResponse:[4,2,1,""],CallerIdentification:[4,2,1,""],IMEI:[4,2,1,""],IMSI:[4,2,1,""],NetworkStatus:[4,2,1,""],PINStatus:[4,2,1,""],SMS:[4,2,1,""],SignalQuality:[4,2,1,""],SubscriberNumber:[4,2,1,""]},"gateway.io.sim800.at_response.NetworkStatus":{Status:[4,2,1,""]},"gateway.io.sim800.at_response.NetworkStatus.Status":{Denied:[4,4,1,""],NotRegistered:[4,4,1,""],RegisteredHome:[4,4,1,""],RegisteredRoaming:[4,4,1,""],Searching:[4,4,1,""],Unknown:[4,4,1,""]},"gateway.io.sim800.at_response.PINStatus":{PHPin:[4,4,1,""],PHPuk:[4,4,1,""],Pin2:[4,4,1,""],Pin:[4,4,1,""],Puk:[4,4,1,""],Ready:[4,4,1,""]},"gateway.io.sim800.at_response.SMS":{Status:[4,2,1,""]},"gateway.io.sim800.at_response.SMS.Status":{Read:[4,4,1,""],Sent:[4,4,1,""],Unread:[4,4,1,""],Unsent:[4,4,1,""]},"gateway.io.sim800.serial_loop":{EchoError:[4,6,1,""],SerialError:[4,6,1,""],SerialLoop:[4,2,1,""]},"gateway.io.sim800.serial_loop.SerialLoop":{run:[4,3,1,""]},"gateway.io.sim800.sim800":{Sim800:[4,2,1,""],Sim800Error:[4,6,1,""]},"gateway.io.sim800.sim800.Sim800":{answer_call:[4,3,1,""],close:[4,3,1,""],dial_number:[4,3,1,""],enter_pin:[4,3,1,""],hang_up_call:[4,3,1,""],hold_call:[4,3,1,""],power_off:[4,3,1,""],request_all_sms:[4,3,1,""],request_imei:[4,3,1,""],request_imsi:[4,3,1,""],request_network_status:[4,3,1,""],request_pin_status:[4,3,1,""],request_signal_quality:[4,3,1,""],request_subscriber_number:[4,3,1,""],request_unread_sms:[4,3,1,""],reset_default_configuration:[4,3,1,""],resume_call:[4,3,1,""],send_sms:[4,3,1,""],set_caller_identification_mode:[4,3,1,""],set_echo_mode:[4,3,1,""],set_error_mode:[4,3,1,""],set_sms_mode:[4,3,1,""],setup:[4,3,1,""],transmit_dtmf_tone:[4,3,1,""],write:[4,3,1,""]},"gateway.networking":{api:[5,0,0,"-"],caller:[5,0,0,"-"],signaling:[5,0,0,"-"],sse:[5,0,0,"-"]},"gateway.networking.api":{API:[5,2,1,""]},"gateway.networking.api.API":{broadcast_notification:[5,3,1,""],close:[5,3,1,""],delete_gateway:[5,3,1,""],get_gateway:[5,3,1,""],get_gateways:[5,3,1,""],get_user:[5,3,1,""],post_gateway:[5,3,1,""],push_error:[5,3,1,""],push_incoming_call:[5,3,1,""],push_notification:[5,3,1,""],put_gateway:[5,3,1,""],put_user:[5,3,1,""],start:[5,3,1,""]},"gateway.networking.caller":{CallError:[5,6,1,""],CallStreamTrack:[5,2,1,""],Caller:[5,2,1,""],Role:[5,2,1,""]},"gateway.networking.caller.CallStreamTrack":{recv:[5,3,1,""]},"gateway.networking.caller.Caller":{is_ongoing:[5,3,1,""],start_call:[5,3,1,""],stop_call:[5,3,1,""]},"gateway.networking.caller.Role":{ANSWER:[5,4,1,""],OFFER:[5,4,1,""]},"gateway.networking.signaling":{AuthenticationError:[5,6,1,""],authenticate:[5,1,1,""],from_ice_candidate:[5,1,1,""],recv_answer:[5,1,1,""],recv_offer:[5,1,1,""],resv_ice_candidate:[5,1,1,""],send_answer:[5,1,1,""],send_offer:[5,1,1,""],to_ice_candidate:[5,1,1,""]},"gateway.networking.sse":{SSE:[5,2,1,""]},"gateway.networking.sse.SSE":{close:[5,3,1,""],connection_state:[5,4,1,""],run:[5,3,1,""]},"gateway.utils":{logger:[6,0,0,"-"],scheduler:[6,0,0,"-"],singleton:[6,0,0,"-"],string_utils:[6,0,0,"-"]},"gateway.utils.logger":{AnsiEscapeSequence:[6,2,1,""],Level:[6,2,1,""],escape_ansi:[6,1,1,""]},"gateway.utils.logger.AnsiEscapeSequence":{BOLD:[6,4,1,""],DEFAULT:[6,4,1,""],FAIL:[6,4,1,""],HEADER:[6,4,1,""],OK_BLUE:[6,4,1,""],OK_GREEN:[6,4,1,""],UNDERLINE:[6,4,1,""],WARNING:[6,4,1,""]},"gateway.utils.logger.Level":{DEBUG:[6,4,1,""],INFO:[6,4,1,""],LOG:[6,4,1,""]},"gateway.utils.scheduler":{Scheduler:[6,2,1,""],Task:[6,2,1,""]},"gateway.utils.scheduler.Scheduler":{run:[6,3,1,""],schedule:[6,3,1,""],schedule_task:[6,3,1,""],stop:[6,3,1,""],stop_task:[6,3,1,""]},"gateway.utils.scheduler.Task":{check_time:[6,3,1,""],execute:[6,3,1,""]},"gateway.utils.singleton":{Singleton:[6,2,1,""]},"gateway.utils.string_utils":{clear_str:[6,1,1,""],split_str:[6,1,1,""],split_str_c:[6,1,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"],"5":["py","staticmethod","Python static method"],"6":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:attribute","5":"py:staticmethod","6":"py:exception"},terms:{"20command":4,"20manual_v1":4,"20series_at":4,"91m":6,"92m":6,"93m":6,"94m":6,"95m":6,"boolean":6,"class":[3,4,5,6],"default":[4,6],"enum":[4,5,6],"function":6,"int":4,"new":[5,6],"return":[4,5,6],"static":4,"try":5,SMS:4,That:6,The:4,Use:6,_compat:[4,5],_id:5,_unixselectoreventloop:[4,5],actual:4,addit:4,addr:3,address:[3,4],address_nam:4,after:6,aiortc:5,alb:3,alert:5,all:4,alpha:4,alphaid:4,ansi:6,ansiescapesequ:6,answer:[4,5],answer_cal:4,api:[0,1,7],arg:[3,6],argument:6,arrai:[4,6],asyncio:4,at_command:[0,2],at_ev:[0,2],at_pars:[0,2],at_respons:[0,2],atcommand:4,atev:4,atpars:4,atrespons:4,attribut:4,audio:5,audiostreamtrack:5,authent:5,authenticationerror:5,base:[3,4,5,6],basic:4,ber:4,bold:6,bool:5,broadcast_notif:5,call:[4,5],callback:4,caller:[0,1,4,7],calleridentif:4,calleridentificationpars:4,callerror:5,callstreamtrack:5,can:4,candid:5,card:4,carriag:6,carrier:5,charact:[4,6],check:[5,6],check_imei:1,check_pin_statu:1,check_tim:6,clear:4,clear_str:6,cli:6,cli_valid:4,client:5,clip:4,close:[4,5],cls:6,cme:4,code:[4,5],colon:6,color:6,com:4,comma:6,command:4,commun:4,compand:3,compateventemitt:[4,5],config:[0,7],configur:4,connect:[3,5],connection_st:5,content:[4,7],core:[0,7],coroutin:[1,4,5],countri:4,cpb:3,creat:6,current:4,custom:4,data:[1,4,5],debug:[4,5,6],decor:6,defin:4,delete_gatewai:5,deni:4,depreci:6,desc:5,descript:5,dev:4,devic:5,device_id:5,dial_numb:4,disabl:[3,4],disconnect:4,dlb:3,document:4,doe:4,doubl:6,download:4,dtmf:4,echo:4,echoerror:4,either:4,elecrow:4,emit:5,emitt:[4,5],enabl:[3,4],encapsul:4,encod:5,enter:4,enter_pin:4,enumer:4,error:[4,5],escap:6,escape_ansi:6,establish:5,event:[4,5],everi:6,except:[4,5],execut:6,extend:4,fail:6,fals:[4,5],firmware_vers:5,first_nam:5,frame:5,from:6,from_ice_candid:5,func:6,furthermor:4,gatewai:7,gateway_imei:5,get:[4,5,6],get_apn_config_path:1,get_config:1,get_gatewai:5,get_us:5,getter:5,given:6,handl:3,hang_up_cal:4,header:6,hold:6,hold_cal:4,host:5,http:4,ice:5,identif:4,ignor:6,imei:4,imeipars:4,implement:[4,6],imsi:4,imsipars:4,incom:4,index:4,indic:6,info:6,init:6,initi:5,intenum:[4,5,6],interfac:4,interv:6,is_ongo:5,iso:4,kwarg:6,lac:4,last_nam:5,level:6,librari:3,line:[4,6],list:4,localhost:5,lock:4,log:6,logger:[0,7],loop:[4,5],main:[0,7],mcc:4,mediastream:5,messag:[4,5],method:5,mnc:4,mode:4,modecontrolregist:3,modul:[0,2,7],more:4,msin:4,must:5,name:4,network:[0,1,4,7],networkstatu:4,networkstatuspars:4,none:[4,5],normal:4,note:5,noth:[4,5,6],notregist:4,null_bit:3,number:[4,5],object:[3,4,5,6],off:4,offer:5,ok_blu:6,ok_green:6,on_answer_cal:1,on_connection_clos:1,on_dial:1,on_enter_pin:1,on_hang_up:1,on_hold_cal:1,on_outgoing_cal:1,on_play_dtmf:1,on_request_sign:1,on_resume_cal:1,on_send_sm:1,on_signaling_timeout:1,one:4,ongo:5,open:5,oper:4,ore:4,output:6,over:4,overrid:4,packag:7,param:6,paramet:[4,5,6],pars:[4,5],parseerror:4,parser:4,particip:4,pass:6,password:5,path:1,pcm:[0,2,5],pcmlib:7,pdf:4,pdu:4,peer:5,ph_sim:4,phone:4,phone_numb:5,phpin:4,phpuk:4,pin2:4,pin:4,pin_requir:5,pinstatu:4,pinstatuspars:4,pleas:6,post_gatewai:5,power:4,power_off:4,process:[4,6],puk2:4,puk:4,push_error:5,push_incoming_cal:5,push_notif:5,put_gatewai:5,put_us:5,pyee:[4,5],qualiti:4,quot:6,read:[3,4],read_fram:3,readi:[4,6],rec:4,receiv:4,recv:5,recv_answ:5,recv_off:5,regist:3,register_control:[0,2],registeredhom:4,registeredroam:4,remot:5,remov:6,repres:4,request:5,request_all_sm:4,request_imei:4,request_imsi:4,request_network_statu:4,request_pin_statu:4,request_signal_qu:4,request_subscriber_numb:4,request_unread_sm:4,reset:[4,6],reset_default_configur:4,respons:4,rest:5,resume_cal:4,resv_ice_candid:5,ring:4,role:5,rssi:4,rtcsessiondescript:5,rtype:6,rule:5,run:[4,5,6],same:[4,6],satyp:4,schedul:[0,7],schedule_task:6,search:4,second:6,semicolon:6,send:[4,5],send_answ:5,send_off:5,send_sm:4,sent:4,sequenc:6,serial0:4,serial:4,serial_loop:[0,2],serial_port:4,serialerror:4,serialloop:4,server:5,servic:4,set:4,set_caller_identification_mod:4,set_config:1,set_echo_mod:4,set_error_mod:4,set_sms_mod:4,setup:4,should:[4,6],shutdown:4,signal:[0,4,7],signal_strength:5,signaling_timeout:5,signalqu:4,signalqualitypars:4,silent:5,sim800:[0,1,2],sim800error:4,sim:[1,4],singleton:[0,7],sleep:6,sms:4,smslistpars:4,socket:5,sourc:[1,3,4,5,6],speed:4,split:6,split_str:6,split_str_c:6,sse:[0,7],start:[1,5],start_cal:5,stat:4,state:5,statu:4,sto:4,stop:6,stop_cal:5,stop_task:6,str:[4,5,6],stream:5,string:6,string_util:[0,7],subaddr:4,subpackag:7,subscrib:4,subscribernumb:4,subscribernumberpars:4,support:4,task:6,text:4,thead:6,thi:[4,5,6],thread:[4,5,6],threadsaf:4,time:[4,6],timeout:5,to_ice_candid:5,tone:4,track:5,transmit:4,transmit_dtmf_ton:4,tri:5,tupl:5,txz:3,type:[4,5,6],underlin:6,unknown:4,unread:4,unsent:4,until:5,urgent:4,use:6,used:6,usernam:5,util:[0,7],verbos:4,voip:5,wait:5,warn:6,webrtc:5,webrtc_timeout:5,websocket:5,when:5,within:4,without:6,wrapper:[3,4,5],write:[3,4],write_fram:3,written:4,www:4,x1b:6},titles:["gateway package","gateway.core package","gateway.io package","gateway.io.pcm package","gateway.io.sim800 package","gateway.networking package","gateway.utils package","Welcome to gatewayw\u2019s documentation!","pcmlib"],titleterms:{api:5,at_command:4,at_ev:4,at_pars:4,at_respons:4,caller:5,config:1,core:1,document:7,gatewai:[0,1,2,3,4,5,6],gatewayw:7,logger:6,main:1,modul:[1,3,4,5,6],network:5,packag:[0,1,2,3,4,5,6],pcm:3,pcmlib:8,register_control:3,schedul:6,serial_loop:4,signal:5,sim800:4,singleton:6,sse:5,string_util:6,subpackag:[0,2],util:6,welcom:7}})