# vsts-cleanup
VSTS tool for cleaning up stuck builds in VSTS

## How to use it?
You will need the following information to run the tool:
* VSTS personal access token (e.g. 'abcd1234'
* VSTS account name (e.g. 'myaccount' in myaccount.visualstudio.com URL)
* VSTS project name (e.g. 'myproject' in myaccount.visualstudio.com/myproject URL)
* Build definition ID (e.g. '1234')
* Build status (e.g. 'postponed', defaults to 'notStarted')

```
python vstscleanup.py -t abcd1234 -a myaccount -p myproject -b 1234 -b postponed
```

Sample output: 
```
INFO:root:About to delete builds with status "notStarted" from "myaccount.visualstudio.com/myproject"
INFO:root:Found "5" builds with status "notStarted"
INFO:root:Delete "https://myaccount.visualstudio.com/[project_guid]/_apis/build/Builds/1"
INFO:root:Delete "https://myaccount.visualstudio.com/[project_guid]/_apis/build/Builds/2"
INFO:root:Delete "https://myaccount.visualstudio.com/[project_guid]/_apis/build/Builds/3"
INFO:root:Delete "https://myaccount.visualstudio.com/[project_guid]/_apis/build/Builds/4"
INFO:root:Done!
```

You can also add ```--dry-run``` to see what the command would do.  
