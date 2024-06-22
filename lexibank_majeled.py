from pathlib import Path
import attr
import pylexibank
from clldutils.misc import slug
from pylexibank import Lexeme, progressbar

import csv
from collections import defaultdict


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "majeled"

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        A `pylexibank.cldf.LexibankWriter` instance is available as `args.writer`. Use the methods
        of this object to add data.
        """
        # Add sources
        args.writer.add_sources()
        args.log.info("Added sources")

        # Add concepts
        concept_map = {}
        for concept in self.concepts:
            idx = f"{concept['NUMBER']}_{slug(concept['ENGLISH'])}"
            args.writer.add_concept(
                ID=idx,
                Name=concept["ENGLISH"],
                Concepticon_ID=concept["CONCEPTICON_ID"],
                Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
            )
            concept_map[concept["ENGLISH"]] = idx
        args.log.info("Added concepts")

        # Add languages
        lang_map = {}
        lang_sources = defaultdict(list)
        for language in self.languages:
            args.writer.add_language(
                ID=slug(language["NAME"]),
                Name=language["NAME"],
                Glottocode=language["GLOTTOCODE"],
            )
            lang_map[language["NAME"]] = slug(language["NAME"])
            lang_sources[language["NAME"]].append(language["SOURCES"])
        args.log.info("Added languages")

        # Add forms
        # Doing things on our own so to deal only as much as necessary with cldfbench/pylexibank
        RAW_PATH = Path(__file__).parent / "raw"
        with open(RAW_PATH / "macro-je.tsv", encoding="utf-8") as csvfile:
            data = list(csv.DictReader(csvfile, delimiter="\t"))
            data = [entry for entry in data if entry["id"]]

        for entry in data:
            idx = entry["id"]
            doculect = entry["DOCULECT"]
            concept = entry["CONCEPT"]
            value = entry["VALUE"]
            form = entry["FORM"]
            cogid = entry["COGID"]
            args.writer.add_form_with_segments(
                Parameter_ID=concept_map[concept],
                Language_ID=lang_map[doculect],
                Value=value,
                Form=form,
                Segments=value.split(),
                Cognacy=cogid,
                # Source="",
            )
