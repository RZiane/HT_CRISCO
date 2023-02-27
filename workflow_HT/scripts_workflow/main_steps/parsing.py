from hopsparser import parser

parser.parse(
        device='cuda',
        in_file='/home/ziane212/crisco_work/ressources/1190_prose/old_13-02-23/1190_Fin_12e_prose_historique_AN_09-11-22.conllu',
        model_path='/home/ziane212/models/SRCMF-flaubert',
        out_file='/home/ziane212/crisco_work/ressources/1190_prose/test.conllu',
        raw=False,
        strict=False
    )



