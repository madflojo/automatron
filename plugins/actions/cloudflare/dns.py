#!/usr/bin/python

import argparse
import json
import logging
import sys
import requests

baseurl = "https://api.cloudflare.com/client/v4"

def validate_response(req):
    ''' General response validation '''
    logger.debug("cloudflare: CloudFlare replied with status code of {0}".format(req.status_code))
    if req.status_code == 200:
        data = json.loads(req.text)
        if data['success'] is True:
            return True
    else:
        logger.debug("cloudflare: Response text: {0}".format(req.text))
        return False

def get_zoneid(email, key, domain):
    ''' Get the ZoneID for the specified domain '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "{0}/zones?name={1}".format(baseurl, domain)
    logger.debug("cloudflare: Requesting url {0}".format(url))
    try:
        req = requests.get(url=url, headers=headers)
        if validate_response(req):
            data = json.loads(req.text)
            for zone in data['result']:
                if zone['name'] == domain:
                    return zone['id']
        else:
            return None
    except:
        return None

def get_recs(email, key, zoneid, page=1, search=None):
    ''' Return a dictionary of records that match searchstring or zoneid '''
    search = search or {}
    return_data = {}
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "{0}/zones/{1}/dns_records?per_page=100".format(baseurl, zoneid)
    for param in search.keys():
        url = "{0}&{1}={2}".format(url, param, search[param])
    if page > 1:
        url = "{0}&page={1}".format(url, page)
    logger.debug("cloudflare: Requesting url {0}".format(url))
    try:
        req = requests.get(url=url, headers=headers)
        if validate_response(req):
            data = json.loads(req.text)
            if data['result_info']['total_pages'] > page:
                newpage = page + 1
                newdata = get_recs(email, key, zoneid, page=newpage, search=search)
                for new in newdata.keys():
                    return_data[new] = newdata[new]
            for rec in data['result']:
                return_data[rec['id']] = rec
        return return_data
    except:
        return return_data

def add_rec(email, key, zoneid, rec):
    ''' Add a new DNS record using the rec dictionary as json data '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "{0}/zones/{1}/dns_records".format(baseurl, zoneid)
    payload = json.dumps(rec)
    try:
        req = requests.post(url=url, headers=headers, data=payload)
        return validate_response(req)
    except:
        return False

def del_rec(email, key, zoneid, recid):
    ''' Delete the specified DNS entry '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "{0}/zones/{1}/dns_records/{2}".format(baseurl, zoneid, recid)
    try:
        req = requests.delete(url=url, headers=headers)
        return validate_response(req)
    except:
        return False

def update_rec(email, key, zoneid, recid, rec):
    ''' Update DNS record '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "{0}/zones/{1}/dns_records/{2}".format(baseurl, zoneid, recid)
    payload = json.dumps(rec)
    try:
        req = requests.put(url=url, headers=headers, data=payload)
        return validate_response(req)
    except:
        return False

if __name__ == "__main__":
    exit_code = 0

    # Start Argument Parser
    parser = argparse.ArgumentParser(
        description="""
CloudFlare DNS Actions

CLI tool for manipulating DNS for CloudFlare hosted domains. This tool uses CloudFlare's v4 API to add, remove,
list, or modify DNS records.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-v", "--verbose", help="Enable verbosity", action="store_true")

    # Action to take
    subparser = parser.add_subparsers(title="Actions", dest='actions')

    # Add Sub Parser
    add_parser = subparser.add_parser(
        "add",
        description="""
Add a new DNS record entry to a CloudFlare protected domain.
        """,
        help="Add DNS Records"
    )
    add_parser.add_argument("email", help="Email address for CloudFlare Authentication")
    add_parser.add_argument("key", help="API Key for CloudFlare Authentication")
    add_parser.add_argument("domain", help="Domain name to modify")
    add_parser.add_argument("name", help="Record name (example: www.example.com)")
    add_parser.add_argument("type", help="Type of record", choices=['A', 'AAAA', 'CNAME', 'MX'])
    add_parser.add_argument(
        "content", help="Record content (example: 10.0.0.1 or cname.example.com.)")
    add_parser.add_argument("--ttl", help="TTL (default: 0)", type=int, default=0)
    add_parser.add_argument(
        "--noproxy", help="Disable CloudFlare proxying",
        action="store_false", default=True)

    # Remove Sub Parser
    remove_parser = subparser.add_parser(
        "remove",
        description="""
Remove DNS records that match specified search criteria.
        """,
        help="Remove DNS records",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group_remove_parser = remove_parser.add_argument_group(
        title="Matching criteria",
        description="""
    Specify which records to remove by using the --name and --content field values.

    Multiple DNS records can be removed by ommiting the --name field. In the example below if the content value of 10.0.0.1
    was provided both record 1 and 3 would be removed.

    Example:
        id    name    content
        --    -----   ---------
        1     www     10.0.0.1
        2     www     10.0.0.2
        3     ftp     10.0.0.1
        """
    )
    remove_parser.add_argument("email", help="Email address for CloudFlare Authentication")
    remove_parser.add_argument("key", help="API Key for CloudFlare Authentication")
    remove_parser.add_argument("domain", help="Domain name to modify")
    group_remove_parser.add_argument(
        "--name", help="Remove records with a matching name (example: www.example.com)")
    group_remove_parser.add_argument("--content", help="Remove records with matching content")

    # Modify Sub Parser
    modify_parser = subparser.add_parser(
        "modify",
        description="""
Modify one or more existing DNS records by replacing the current record with the new 'type' and 'content'. This action uses
the 'old_content' field to search for DNS records to modify. If --name is used only the record named will be modified.
        """,
        help="Modify existing records",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    modify_parser.add_argument("email", help="Email address for CloudFlare Authentication")
    modify_parser.add_argument("key", help="API Key for CloudFlare Authentication")
    modify_parser.add_argument("domain", help="Domain name to modify")
    modify_parser.add_argument(
        "old_content",
        help="Previous record content (example: 10.0.0.1 or cname.example.com.)"
    )
    modify_parser.add_argument(
        "type", help="Type of record for new record", choices=['A', 'AAAA', 'CNAME', 'MX'])
    modify_parser.add_argument(
        "new_content",
        help="New record content (example: 10.0.0.1 or cname.example.com.)"
    )
    modify_parser.add_argument("--name", help="Record name (example: www.example.com)")

    # List Sub Parser
    list_parser = subparser.add_parser(
        "list",
        description="""
List existing DNS records that match the defined criteria.
        """,
        help="List existing records",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group_list_parser = list_parser.add_argument_group(
        title="Matching criteria",
        description="""
    Output can be limited by using the matching criteria to limit the search to records that match the values
    provided.

    If no matching criteria is provided than all DNS records will be listed.
        """
    )
    list_parser.add_argument("email", help="Email address for CloudFlare Authentication")
    list_parser.add_argument("key", help="API Key for CloudFlare Authentication")
    list_parser.add_argument("domain", help="Domain name to modify")
    group_list_parser.add_argument(
        "--name", help="List records with a matching name (example: www.example.com)")
    group_list_parser.add_argument(
        "--type", help="Type of record", choices=['A', 'AAAA', 'CNAME', 'MX'])
    group_list_parser.add_argument("--content", help="List records with matching content")

    # Parse Arguments
    args = parser.parse_args()

    # Setup logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s]: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    # Clear requests logging
    logging.getLogger("requests").setLevel(logging.WARNING)

    # If verbose enable DEBUG logging
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Fetch ZoneID
    zoneid = get_zoneid(args.email, args.key, args.domain)

    # Start Actioning
    if args.actions == "list": # Action: List DNS Records
        # Setup matching criteria
        search = {}
        if args.content:
            search.update({'content': args.content})
        if args.type:
            search.update({'type': args.type})
        if args.name:
            search.update({'name': args.name})
        # Get zone id then get records
        recs = get_recs(args.email, args.key, zoneid, search=search)
        # Build list of lists
        records = []
        for rec_id in recs.keys():
            records.append([
                rec_id,
                recs[rec_id]['name'],
                recs[rec_id]['type'],
                recs[rec_id]['content']
            ])
        # Print columned output
        for header in ["ID", "Name", "Type", "Content"]:
            print "{0}".format(header).ljust(40),
        print ""
        for line in records:
            for item in line:
                # Truncate values after 38 characters
                print "{0}".format(item[:38]).ljust(40),
            print ""
    elif args.actions == "add": # Action: Add DNS Records
        result = add_rec(
            args.email,
            args.key,
            zoneid,
            {
                'name': args.name,
                'type': args.type,
                'content': args.content,
                'proxied': args.noproxy
            }
        )
        if result:
            logger.info("Successfully created new DNS record")
            sys.exit(0)
        else:
            logger.critical("Failed to create new DNS record")
            sys.exit(1)
    elif args.actions == "remove": # Action: Remove DNS Records
        # Setup matching criteria
        search = {}
        matched = False
        if args.content:
            search.update({'content': args.content})
            matched = True
        if args.name:
            search.update({'name': args.name})
            matched = True
        # Verify we have a matching criteria to search with
        if matched is False:
            logger.critical("Can't find records without matching criteria")
            parser.print_help()
            sys.exit(1)
        # Get records
        recs = get_recs(args.email, args.key, zoneid, search=search)
        for record in recs.keys():
            if del_rec(args.email, args.key, zoneid, record):
                logger.info("Removed record: {0} {1} {2}".format(
                    recs[record]['name'],
                    recs[record]['type'],
                    recs[record]['content']
                ))
            else:
                logger.critical("Failed to remove record: {0} {1} {2}".format(
                    recs[record]['name'],
                    recs[record]['type'],
                    recs[record]['content']
                ))
                exit_code = 1
    elif args.actions == "modify": # Action: Update DNS Records
        search = {'content': args.old_content}
        if args.name:
            search.update({'name': args.name})
        # Get records
        recs = get_recs(args.email, args.key, zoneid, search=search)
        for record in recs.keys():
            results = update_rec(
                args.email,
                args.key,
                zoneid,
                record,
                {
                    'type': args.type,
                    'content': args.new_content,
                    'name': recs[record]['name']
                },
            )
            if results:
                logger.info("Updated record: {0} {1} {2} > {3} {4}".format(
                    recs[record]['name'],
                    recs[record]['type'],
                    recs[record]['content'],
                    args.type,
                    args.new_content
                ))
            else:
                logger.critical("Failed to update record: {0} {1} {2}".format(
                    recs[record]['name'],
                    recs[record]['type'],
                    recs[record]['content']
                ))
                exit_code = 1
    # Indicate whether everything worked or not
    sys.exit(exit_code)
