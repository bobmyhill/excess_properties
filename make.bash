#!/bin/bash

base=excess_properties

pdflatex ${base}
bibtex ${base}
pdflatex ${base}
pdflatex ${base}