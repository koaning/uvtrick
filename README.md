<img src="docs/highlight.png" width="125" height="125" align="right" />

### Sentence Models

> A different take on textcat.

## Quickstart 

You can install this tool via: 

```
python -m pip install sentence-models 
```

Then from there you can train a sentence model and apply it via: 

```python
from sentence_models import SentenceModel

# Learn a new sentence-model. This `.jsonl` data needs to be in the right format.
smod = SentenceModel().learn_from_disk("annotations.jsonl")

# Make a prediction
example = "In this paper we introduce a new dataset for citrus fruit detection. We also contribute a state of the art algorithm."
smod(example)
```

To learn more about the expected data format of a sentence-model, check [the docs](https://koaning.github.io/sentence-models/).

## Why sentence models? 

I was working on a project that tries to detect topics in academic articles found on arxiv. One of the topics I was interested in was "new datasets". If an article presents a new dataset there's usually something interesting happening so I wanted to build a classifier for it. 

![](docs/img1.jpeg)

You could build a classifier on the entire text and that could work, but it takes _a lot_ of effort to annotate because you'd need to read the entire abstract. It's probably hard for an algorithm too. It has to figure out what part of the abstract is important for the topic of interest and there's a lot of text that might matter. 

But what if we choose to approach the problem slightly differently?

![](docs/img2.jpeg)

Maybe it makes sense to split the text into sentences and run a classifier on each one of those. This might not be perfect for _every_ scenario out there. But it seems like a valid starting point to help you annotate and get started. 

If you have sentence level predictions, you could re-use that to do abstract-level predictions.

![](docs/sentence-model.png)

This approach may not be perfect, but it seemed _so_ much easier to annotate sentences ... that we might also want to model that way. 

## Documentation 

Did this make you curious? Check out [the docs](https://koaning.github.io/sentence-models/) for a more in-depth quickstart! 
