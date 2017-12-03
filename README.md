## Transaction Description Normaliser
The key purpose of this library is to take care of string normalisation.
 
*tnormaliser.StringNormalizer(keep_stopwords=False, keep_punctuation=False, lowercase=True, short_state_names=True, full_city_names=True, remove_nonalnum=True, disamb_country_names=True, ints_to_words=True, year_to_label=True)*

* **keep_stopwords**: *boolean, default False*

    ```Specifies whether or not the English stopwords should be removed```
* **keep_punctuation**: *boolean, default False*

    ```Specifies if you want to remove punctuation```
    
* **lowercase**: *boolean, default True*

    ```Specifies whether make the string lower case```
* **short_state_names**: *boolean, default True*
	
	```Should the long Australian state names be replaced with abbreviations? Example: New South Wales or NSW```
	
* **full_city_names**: *boolean, default True*

	```Should various shortened forms of Australian city names be replaced with the corresponding full names, e.g. should we have Brisbane instead of Bris```
	
* **remove_nonalnum**: *boolean, default True*

	```Do the non-alphanumeric characters need to be removed?```
	
* **disamb_country_names**: *boolean, default True*

	```Some countries are known by a few names. Should we make sure that a single name is used in our string?```
	
* **ints_to_words**: *boolean, default True*

	```Specify whether integers should be converted to words```
	
* **year_to_label**: *boolean, default True*

	```Should all years mentioned in the string be replaced with a placeholder !YEAR!?```
	
#### Usage: 
> tnormaliser.StringNormalizer().normalise(string)
	