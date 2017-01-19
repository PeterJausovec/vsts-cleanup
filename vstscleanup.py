import argparse
import base64
import logging

import requests


def _get_headers(vsts_token):
    """
    Gets the header to use for making VSTS API calls
    """
    b64token = base64.b64encode(':' + vsts_token)
    return {'Authorization': 'Basic ' + b64token, 'content-type': 'application/json'}

def get_arg_parser():
    """
    Sets up the arg parser
    """
    parser = argparse.ArgumentParser(description='VSTS Cleanup - cleans up VSTS builds',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', help='VSTS Personal Access Token', dest='vsts_token')
    parser.add_argument('-a', help='VSTS Account Name', dest='account_name')
    parser.add_argument('-p', help='VSTS Project Name', dest='project_name')
    parser.add_argument('-b', help='Build definition ID (E.g. 1234)', dest='build_definition_id')
    parser.add_argument('-s', help='Build status (e.g. inProgress, completed, cancelling, postponed, notStarted, all)',
                        dest='build_status', default='notStarted')
    parser.add_argument('--dry-run', help='Do a dry run, don\'t delete anything',
                        action='store_true', default=False)
    return parser

def process_arguments():
    """
    Process the arguments
    """
    arg_parser = get_arg_parser()
    arguments = arg_parser.parse_args()

    if arguments.vsts_token is None:
        arg_parser.error('VSTS token (-t) is required')
    if arguments.account_name is None:
        arg_parser.error('Account name (-a) is required')
    if arguments.project_name is None:
        arg_parser.error('Project name (-p) is required')
    if arguments.build_definition_id is None:
        arg_parser.error('Build definition ID (-b) is required')

    return arguments

def _delete_build(headers, build_url):
    """
    Deletes the VSTS build using the provided URL
    """
    logging.info('Delete "%s"', build_url)
    delete_response = requests.delete(build_url + '?api-version=1.0', headers=headers)
    delete_response.raise_for_status()

def _get_build_url(account_name, project_name, build_def_id, build_status):
    """
    Gets the build URL
    """
    url = 'https://{}.visualstudio.com/{}/_apis/build/builds?api-version={}&definitions={}&statusFilter={}'.format(
        account_name, project_name, '2.0', build_def_id, build_status)
    return url

def _get_all_builds(auth_headers):
    """
    Gets all builds from VSTS
    using the provided URL
    """
    url = _get_build_url(
        args.account_name, args.project_name, args.build_definition_id, args.build_status)
    response = requests.get(url, headers=auth_headers)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    args = process_arguments()
    logging.root.setLevel(logging.INFO)

    if args.dry_run:
        logging.info('DRY RUN; nothing will be deleted')

    logging.info('About to delete builds with status "%s" from "%s.visualstudio.com/%s"',
                 args.build_status,
                 args.account_name,
                 args.project_name)

    headers = _get_headers(args.vsts_token)
    all_builds = _get_all_builds(headers)

    logging.info('Found "%s" builds with status "%s"', all_builds['count'], args.build_status)
    for build in all_builds['value']:
        build_url = build['url']
        if not args.dry_run:
            _delete_build(headers, build_url)
    logging.info('Done!')
