import streamlit as st
import myvariant
import hgvs.parser


st.set_page_config(page_title='MyVariant')

st.header('MVZ Freiburg')
st.markdown('by Oskar Schnappauf')
st.subheader('Arbeit mit Varianten')
expander_variants = st.expander('variants')
variant_coordinates = st.text_input("Füge hier deine Variante ein", placeholder='chr7:g.140453134T>C')
if variant_coordinates:
    mv = myvariant.MyVariantInfo()
    if isinstance(mv.getvariant(variant_coordinates), dict):
        my_variant = mv.getvariant(variant_coordinates)
        available_info = []
        for key in my_variant.keys():
            available_info.append(key)
        st.write(available_info)
        #st.markdown(f"{my_variant['snpeff']['ann']['feature_id']}({my_variant['snpeff']['ann']['genename']}):{my_variant['snpeff']['ann']['hgvs_c']} ({my_variant['snpeff']['ann']['hgvs_p']})")
        try:
            st.markdown(f"{my_variant['clinvar']['rcv'][0]['preferred_name']}")
        except KeyError:
            st.markdown(f"Variante nicht in ClinVar")
        gnomad_maf_ex = my_variant['gnomad_exome']['af']['af']
        gnomad_het_ex = my_variant['gnomad_exome']['ac']['ac']
        gnomad_hom_ex = my_variant['gnomad_exome']['hom']['hom']
        gnomad_maf_ge = my_variant['gnomad_genome']['af']['af']
        gnomad_het_ge = my_variant['gnomad_genome']['ac']['ac']
        gnomad_hom_ge = my_variant['gnomad_genome']['hom']['hom']
        gnomad_maf_ex_exp = '{:.2e}'.format(gnomad_maf_ex)
        st.markdown(f"Die MAF der Variante in gnomAD ist {gnomad_maf_ex_exp}.")
        st.markdown(f'Die Variante liegt {gnomad_het_ex}x heterozygot in gnomAD vor')
        st.markdown(f'Die Variante liegt {gnomad_hom_ex}x homozygot in gnomAD vor')
        st.markdown(f'Die Variante liegt {gnomad_het_ge}x heterozygot in gnomAD vor')
        st.markdown(f'Die Variante liegt {gnomad_hom_ge}x homozygot in gnomAD vor')
        st.markdown(f"Die Variante ist in dbSNP gelistet mit der id: {my_variant['dbsnp']['dbsnp_merges']['rsid']}")
        st.markdown(f"Die Mutationtaster-Vorhersage ist {my_variant['dbnsfp']['mutationtaster']}")
        st.write(mv.getvariant(variant_coordinates, fields='all'))
        #st.write(mv.getvariant(variant_coordinates),fields='cadd.phred,dbsnp.rsid')
    else:
        st.markdown('Kann Variante nicht finden, sorry!')
