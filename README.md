# BrikoCorpus

Briko Corpus comprises content extracted from news websites such as SINA.COM, LSSDJT.COM, TMTPOST.COM, etc.
The raw content is filtered and sorted in the aim of improve the quality for machine-learning purposes.

Briko Corpus can be downloaded [here](https://linktobe.added)

The filtering script [ApplyFilter.py](./ApplyFilter.py) is provided for your reference. 

You can also use [GetSample.py](./GetSample.py) to extract random samples of the corpus for testing purpose.

GetSample.py Usage:
```python
python GetSample.py -num_samples 100 -corpus_path FinalContent.txt -sample_path SampleCorpus.txt
```
