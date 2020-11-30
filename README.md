# Isogeny database

This is the public repository for our [isogeny database](https://isogenies.enricflorit.com/), originally presented at the [BYMAT2020](https://bymat.webs.upv.es/index/) poster session.


⚠️**WIP**⚠️

---
Our code uses [Lithops](https://github.com/lithops-cloud/lithops), we encourage you to read their documentation to learn how to set it up on your computer.

If you just want to run the script on your computer, the standard `multiprocessing` python's library can be used by just changing two import lines of the script:

``` python
from lithops.multiprocessing import Pool
from lithops.storage.cloud_proxy import open, os 
```

Change to:

``` python
from multiprocessing import Pool
import os 
```
