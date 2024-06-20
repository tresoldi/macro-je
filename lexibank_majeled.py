from pathlib import Path
import attr
import pylexibank
from clldutils.misc import slug
from pylexibank import Lexeme, progressbar

import csv

class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "majeled"

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        A `pylexibank.cldf.LexibankWriter` instance is available as `args.writer`. Use the methods
        of this object to add data.
        """
        #args.writer.add_sources()


        # Doing things on our own so to deal only as much as necessary with cldfbench/pylexibank
        RAW_PATH = Path(__file__).parent / "raw"
        with open(RAW_PATH/"macro-je.tsv", encoding="utf-8") as csvfile:
            data = list(csv.DictReader(csvfile, delimiter="\t"))
            data = [entry for entry in data if entry["id"]]

        #for row in data:
        #    print(row)

        # Add concepts
        for concept in self.concepts:
            idx = f"{concept['NUMBER']}_{slug(concept['ENGLISH'])}"
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["ENGLISH"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
                    )
        args.log.info("Added concepts")


        # Add languages
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["NAME"],
                    Glottocode=language["GLOTTOCODE"])
        args.log.info("Added languages")

        #data = self.raw_dir.read_csv(
        #        'SupMaterials2_RawLinguisticForms.Blad2.csv'
        #        )
        #sources = {k: v for k, v in self.raw_dir.read_csv('ref_to_bib.csv')}
        #languages_in_row = data[0][1:]

        a = """
        data += [['']]
        for i in progressbar(range(6, 2751, 8)):
            concept = data[i][0]
            for j, language in enumerate(languages_in_row):
                value = data[i][j+1]
                if value.strip():
                    form = data[i+2][j+1].replace(' ', '_').split('/')[0]
                    classes = data[i+3][j+1]
                    
                    source = sources.get(data[5][j+1].strip(), '')
                    args.writer.add_forms_from_value(
                            Language_ID=languages[language],
                            Parameter_ID=concepts[concept],
                            Orthography=value,
                            Value=form,
                            SoundClasses=classes,
                            Source=source
                            )
    """

