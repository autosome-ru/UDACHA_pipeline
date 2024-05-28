# UDACHA pipline

This repository contains code used to build a ![database](https://udacha.autosome.org/IceKing) of allele-specific chromatin accessibility sites.

1. The SNP calling step is performed by the https://github.com/autosome-ru/ADASTRA-pipeline using GATK
2. Grouping according to cell types performed by scripts/advanced_badgroups/plink_clustering.sh using [plink2](https://www.cog-genomics.org/plink/2.0/)
3. Group-specific BAD reconstruction is performed by scripts/advanced_badgroups/make_advanced_badgroups.py using [BABACHI](https://github.com/autosome-ru/BABACHI)
4. ASE calling is performed by scripts/mixalime/make_release.sh using [MIXALIME](https://github.com/autosome-ru/MixALime)



