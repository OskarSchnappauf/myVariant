import streamlit as st
import myvariant
import pandas as pd
#import hgvs.parser


st.set_page_config(page_title='MyVariant')

st.header('MVZ Freiburg')
st.markdown('by Oskar Schnappauf')
st.subheader('Arbeit mit Varianten')
expander_variants = st.expander('variants')
df_hgnc = pd.read_csv('HGNC_genes_11_04_2022.txt', sep="\t")
d = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
st.dataframe(df_hgnc)
coordinates = st.text_input("Füge hier deine Variante ein", placeholder='chr7:140453134T>C')
variant_coordinates = coordinates.replace(":", ":g.")
if variant_coordinates:
    mv = myvariant.MyVariantInfo()
    if isinstance(mv.getvariant(variant_coordinates), dict):
        my_variant = mv.getvariant(variant_coordinates)
        available_info = []
        for key in my_variant.keys():
            available_info.append(key)
        st.markdown(available_info)
        st.write(my_variant['snpeff']['ann'])


        #gene_symbol = my_variant['snpeff']['ann']['genename']
        #df_gene_user = df_hgnc[df_hgnc['Approved symbol'].str.contains(gene_symbol, na=False)]
        #MANE_transcript = df_gene_user['MANE Select RefSeq transcript ID (supplied by NCBI)'].iloc[0]

        st.markdown(f'**Beschreibung**')
        st.markdown(my_variant['snpeff']['ann']['hgvs_p'])
        st.markdown(f"{my_variant['snpeff']['ann']['feature_id']}({my_variant['snpeff']['ann']['genename']}):{my_variant['snpeff']['ann']['hgvs_c']} ({my_variant['snpeff']['ann']['hgvs_p']})")
        st.markdown(f'Für das Gen {gene_symbol} gibt es ein MANE-Transkript: {MANE_transcript}. Siehe auch Morales et al., 2022')

        st.markdown(f'**ClinVar**')
        if 'clinvar' in available_info:
            st.markdown(f"{my_variant['clinvar']['rcv'][0]['preferred_name']}")
        else:
            st.markdown(f"Variante nicht in ClinVar")

        if 'gnomad_exome' in available_info:
            gnomad_maf_ex = my_variant['gnomad_exome']['af']['af']
            gnomad_het_ex = my_variant['gnomad_exome']['ac']['ac']
            gnomad_hom_ex = my_variant['gnomad_exome']['hom']['hom']
            gnomad_maf_ex_exp = '{:.2e}'.format(gnomad_maf_ex)
            st.markdown(f'**gnomAD Exom**')
            st.markdown(f'MAF: {gnomad_maf_ex_exp}; {gnomad_het_ex}x heterozygot; {gnomad_hom_ex}x homozygot')
            #st.markdown(f'Die Variante liegt {gnomad_het_ex}x heterozygot in gnomAD vor')
            #st.markdown(f'Die Variante liegt {gnomad_hom_ex}x homozygot in gnomAD vor')
        else:
            st.markdown(f"Die Variante liegt nicht in der gnomAD (Exomes) Datenbank vor")

        if 'gnomad_genome' in available_info:
            gnomad_maf_ge = my_variant['gnomad_genome']['af']['af']
            gnomad_het_ge = my_variant['gnomad_genome']['ac']['ac']
            gnomad_hom_ge = my_variant['gnomad_genome']['hom']['hom']
            gnomad_maf_ge_exp = '{:.2e}'.format(gnomad_maf_ge)
            st.markdown(f'**gnomAD Genom**')
            st.markdown(f'MAF: {gnomad_maf_ge_exp}; {gnomad_het_ge}x heterozygot; {gnomad_hom_ge}x homozygot')

            #st.markdown(f"Die MAF der Variante in gnomAD (Exomes) ist {gnomad_maf_ge_exp}.")
            #st.markdown(f'Die Variante liegt {gnomad_het_ge}x heterozygot in gnomAD vor')
            #st.markdown(f'Die Variante liegt {gnomad_hom_ge}x homozygot in gnomAD vor')
        else:
            st.markdown(f"Variante nicht in gnomAD Genom Datenbank")

        if 'gnomad_genome' and 'gnomad_exome' in available_info:
            gnomad_het_mut_total = (my_variant['gnomad_exome']['ac']['ac']) + (my_variant['gnomad_genome']['ac']['ac'])
            gnomad_het_wt_total = (my_variant['gnomad_exome']['an']['an']) + (my_variant['gnomad_genome']['an']['an'])
            gnomad_hom_total = (my_variant['gnomad_exome']['hom']['hom']) + (my_variant['gnomad_genome']['hom']['hom'])

            MAF_total = gnomad_het_mut_total/gnomad_het_wt_total
            MAF_total_final = gnomad_maf_ge_exp = '{:.2e}'.format(MAF_total)
            st.markdown(f'**gnomAD gesamt**')
            st.markdown(f'MAF: {MAF_total_final}; {gnomad_het_mut_total}x heterozygot; {gnomad_hom_total}x homozygot')

            #st.write(MAF_total_final)


        if 'dbnsfp' in available_info:
            st.markdown(f"Die Mutationtaster-Vorhersage ist {my_variant['dbnsfp']['mutationtaster']}")
        st.write(mv.getvariant(variant_coordinates, fields='all'))
        #st.write(mv.getvariant(variant_coordinates),fields='cadd.phred,dbsnp.rsid')
    else:
        st.markdown('Kann Variante nicht finden, sorry!')
