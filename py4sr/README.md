![GSI Logo](http://gsi.dit.upm.es/templates/jgsi/images/logo.png)
[simrec](http://gsi.dit.upm.es)
==================================

##Introduction

simrec implements a case-based recommendation system which mainly use similarity as core for
recommendation. The case-based recommendation system is a kind of content-based recommendation system which
mainly use the item content for recommending similar items. Different from the conventional 
content-based recommendation system where the item descriptions are modeled as Vector Space of 
word frequency. The case-based recommendation system constructs the item description in a structured
way, where each feature represents an attribute and has a corresponding type. The items are recommended 
according to the similarities between them. The similarities are computed based on specific similarity metric 
defined by user.

##Similarity Config

To start a recommender, you need to create a similarity config first according to your data
structure. In simrec, several similarity metrics have been implemented, you need to assign them to the specific field.
Suppose your item description has four fields which are name, area, population, and geo, you can define them in config
like below. Also, you are able to config the weight together with each field as well in order to
differ the different contribution of each feature.
```
config = []
config.append({'sim':'string','weight':0.25, 'field':'name'})
config.append({'sim':'numeric','weight':0.25, 'field':'area'})
config.append({'sim':'numeric','weight':0.25, 'field':'population'})
config.append({'sim':'taxonomy','weight':0.25, 'field':'geo'})
```


## Construct the similarity configuration



About this repository
------------------------------
For more information, contact us through: http://gsi.dit.upm.es
