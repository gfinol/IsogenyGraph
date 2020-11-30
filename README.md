# Isogeny database

This is the public repository for our [database](https://isogenies.enricflorit.com/) poster presented at [BYMAT2020](https://bymat.webs.upv.es/index/).


⚠️**WIP**⚠️

---
Our code uses [Lithops](https://github.com/lithops-cloud/lithops), to learn how to setup lithops on your computer we encounrage to visit their documentation.

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
