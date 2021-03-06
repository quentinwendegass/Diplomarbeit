//
//  ContactsTableViewController.swift
//  SIMplePhone
//
//  Created by Lukas Kuster on 30.10.18.
//  Copyright © 2018 Lukas Kuster. All rights reserved.
//

import UIKit
import Contacts
import ContactsUI
import SwiftMessages
import SIMplePhoneKit
import PhoneNumberKit

class ContactsTableViewController: UITableViewController, UISearchBarDelegate {
    
    var resultSearchController = UISearchController()
    var filteredContacts = [CNContact]()
    
    var contacts = [String: [CNContact]]()
    var contactsSections = Array<String>()
    
    var contactStore = CNContactStore()
    var specificGroup: CNGroup? {
        didSet {
            self.fetchContacts()
        }
    }
    
    private func fetchContacts() {
        self.contacts = [:]
        self.contactsSections = []
        
        contactStore.requestAccess(for: (.contacts)) { (granted, err) in
            if let err = err {
                print("Failed to request access", err)
                return
            }
            
            if granted {
                let keys = [CNContactViewController.descriptorForRequiredKeys()]
                let fetchRequest = CNContactFetchRequest(keysToFetch: keys)
                
                fetchRequest.sortOrder = CNContactSortOrder.userDefault
                
                do {
                    if let group = self.specificGroup {
                        let predicate = CNContact.predicateForContactsInGroup(withIdentifier: group.identifier)
                        let contacts = try self.contactStore.unifiedContacts(matching: predicate, keysToFetch: keys)
                        
                        for contact in contacts {
                            self.addContactToArray(contact)
                        }
                    }else{
                    
                        try self.contactStore.enumerateContacts(with: fetchRequest, usingBlock: { (contact, error) in
                            self.addContactToArray(contact)
                        })
                    }
                    
                    DispatchQueue.main.async {
                        self.tableView.reloadData()
                    }
                    
                }
                catch let error as NSError {
                    print(error.localizedDescription)
                }
                
            }else{
                print("Access denied!")
            }
        }
        
    }
    
    func addContactToArray(_ contact: CNContact) {
        var sectionLetter = ""
        if contact.familyName != "" {
            sectionLetter = String(contact.familyName.first!).uppercased()
        }else if contact.organizationName != "" {
            sectionLetter = String(contact.organizationName.first!).uppercased()
        }else{
            
        }
        if sectionLetter != "" {
            if self.contacts[sectionLetter] != nil {
                self.contacts[sectionLetter]?.append(contact)
            }else{
                self.contactsSections.append(sectionLetter)
                self.contacts[sectionLetter] = [contact]
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.navigationController?.navigationBar.prefersLargeTitles = true
        
        self.navigationItem.rightBarButtonItem = UIBarButtonItem(image: #imageLiteral(resourceName: "number_pad"), style: .done, target: self, action: #selector(didTapDialpadBtn))
        
        self.resultSearchController = ( {
            let controller = UISearchController(searchResultsController: nil)
            controller.searchResultsUpdater = self
            controller.dimsBackgroundDuringPresentation = false
            controller.hidesNavigationBarDuringPresentation = false
            controller.searchBar.sizeToFit()
            controller.searchBar.delegate = self
            self.navigationItem.searchController = controller
            self.navigationItem.hidesSearchBarWhenScrolling = false
            return controller
        })()
        
        self.fetchContacts()
    }
    
    @objc func didTapDialpadBtn() {
        let dialpadVC = DialpadViewController()
        dialpadVC.delegate = self
        let navVc = UINavigationController(rootViewController: dialpadVC)
        let seque = DialpadSegue(identifier: nil, source: self, destination: navVc)
        seque.perform()
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        if resultSearchController.isActive { return 1 }
        return contactsSections.count
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if resultSearchController.isActive { return self.filteredContacts.count }
        return contacts[contactsSections[section]]?.count ?? 0
    }
    
    override func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        if resultSearchController.isActive { return nil }
        return contactsSections[section]
    }
    
    override func sectionIndexTitles(for tableView: UITableView) -> [String]? {
        if resultSearchController.isActive { return nil }
        return contactsSections
    }

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ContactCell", for: indexPath)
        
        var contact: CNContact
        if resultSearchController.isActive {
            contact = filteredContacts[indexPath.row]
        }else{
            let section = self.contacts[self.contactsSections[indexPath.section]]
            contact = section![indexPath.row]
        }
        
        cell.textLabel?.attributedText = contact.attributedFullName()
        return cell
    }
    
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        var selectedContact: CNContact
        if resultSearchController.isActive {
            selectedContact = filteredContacts[indexPath.row]
        }else{
            let section = self.contacts[self.contactsSections[indexPath.section]]
            selectedContact = section![indexPath.row]
        }
        
        let contactView = CNContactViewController(for: selectedContact)
        contactView.delegate = self
        self.navigationController?.pushViewController(contactView, animated: true)
    }
    
    // MARK: - Navbar Actions
    @IBAction func didTapGroupsBtn(_ sender: UIBarButtonItem) {
        do {
            let groups = try contactStore.groups(matching: nil)
            
            let alert = UIAlertController()
            
            let allGroups = UIAlertAction(title: "All Groups", style: .default) { (_) in
                self.specificGroup = nil
            }
            if self.specificGroup == nil {
                if allGroups.value(forKey: "checked") != nil {
                    allGroups.setValue(true, forKey: "checked")
                }
            }
            
            alert.addAction(allGroups)
            for group in groups {
                let action = UIAlertAction(title: group.name, style: .default) { (_) in
                    self.specificGroup = group
                }
                if group == self.specificGroup {
                    if action.value(forKey: "checked") != nil {
                        action.setValue(true, forKey: "checked")
                    }
                }
                alert.addAction(action)
            }
            alert.addAction(UIAlertAction(title: "Dismiss", style: .cancel, handler: nil))
            alert.popoverPresentationController?.barButtonItem = sender
            self.present(alert, animated: true, completion: nil)

        } catch let error as NSError {
            print(error.localizedDescription)
        }
        
    }
    
    @IBAction func didTapAddContactBtn(_ sender: UIBarButtonItem) {
        self.addNewContact()
    }
    
    func addNewContact(withNumber number: SPNumber? = nil) {
        let contact = CNMutableContact()
        if let number = number {
            let homePhone = CNLabeledValue(label: CNLabelHome, value: CNPhoneNumber(stringValue: number.phoneNumber))
            contact.phoneNumbers = [homePhone]
        }
        let contactView = CNContactViewController(forNewContact: contact)
        contactView.contactStore = self.contactStore
        contactView.delegate = self
        let navController = UINavigationController(rootViewController: contactView)
        self.present(navController, animated:true, completion: nil)
    }
    
    func initiateCall(with contact: CNContact, _ property: CNContactProperty, parent: CNContactViewController) {
        do {
            let phoneNumber = (property.value as! CNPhoneNumber).stringValue
            let phonenumberkit = PhoneNumberKit()
            let pnkNumber = try phonenumberkit.parse(phoneNumber)
            let fNumber = phonenumberkit.format(pnkNumber, toType: .e164)
            let number = SPNumber(withNumber: fNumber)
            SPDelegate.shared.initiateCall(with: number)
        } catch let error as NSError {
            print(error.localizedDescription)
        }
    }
}

extension ContactsTableViewController: CNContactViewControllerDelegate {
    func contactViewController(_ viewController: CNContactViewController, didCompleteWith contact: CNContact?) {
        viewController.dismiss(animated: true) {
            self.fetchContacts()
        }
    }
    
    func contactViewController(_ viewController: CNContactViewController, shouldPerformDefaultActionFor property: CNContactProperty) -> Bool {
        if property.key == "phoneNumbers" {
            self.initiateCall(with: viewController.contact, property, parent: viewController)
            return false
        }else{
            return true
        }
    }
}

extension ContactsTableViewController: DialpadViewControllerDelegate {
    func dialpadViewController(didRequestCall to: SPNumber) {
        SPDelegate.shared.initiateCall(with: to)
    }
    
    func dialpadViewController(didRequestNewContact with: SPNumber) {
        self.addNewContact(withNumber: with)
    }
    
    func dialpadViewController(didRequestContactViewFor contact: CNContact) {
        let contactView = CNContactViewController(for: contact)
        contactView.delegate = self
        self.navigationController?.pushViewController(contactView, animated: true)
    }
}

extension ContactsTableViewController: UISearchResultsUpdating {
    func updateSearchResults(for searchController: UISearchController) {
        if let searchText = resultSearchController.searchBar.text, searchController.isActive {
            let predicate: NSPredicate
            if searchText.count > 0 {
                predicate = CNContact.predicateForContacts(matchingName: searchText)
            }else{
                filteredContacts = []
                self.tableView.reloadData()
                return
            }
            
            let store = CNContactStore()
            do {
                let keys = [CNContactViewController.descriptorForRequiredKeys()]
                filteredContacts = try store.unifiedContacts(matching: predicate,
                                                             keysToFetch: keys)
                
                self.tableView.reloadData()
                
            }
            catch {
                print("Error!")
            }
        }
        self.tableView.reloadData()
    }
}
