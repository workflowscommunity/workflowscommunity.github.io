---
layout: working_groups
title: "WfBG: Workflow Benchmarking Group"
description: Define methodology to collect meaningful performance metrics; share exemplar workflows written in multiple workflow languages
status: Establishing
join: TODO
members:
    - name: Iacopo Colonnelli
      role: Chair
      link: https://orcid.org/0000-0001-9290-2017
    - name: Michael R. Crusoe
      role: Chair
      link: https://orcid.org/0000-0002-2961-9670
    - name: Rafael Ferreira da Silva
      link: https://orcid.org/0000-0002-1720-0928
---

## Goals

In this working group, we seek to:
- Define a **shared vocabulary of performance metrics** of interest for diverse workflow domains
- Design, maintain and share **benchmarking suites of real-world workflows** to help evaluate those metrics
- Develop **community agreement on features** that such benchmarks should possess
- Collaboratively maintain a **catalogue of state-of-art implementations** of these real-world workflows for various workflow languages/frameworks.
- Define a **reproducible and agnostic methodology** to collect and report benchmark results

## Anti-Goals

We do NOT aim to do any of the following:
- Test workflows using **minimized data sets** that are not representative of actual workflow uses
- Define **which performance metrics are essential** for the workflow research domain. Instead, we want to define several benchmarking suites to evaluate
  different metrics
- Determine the **universally best tool** for running workflows. Instead, we want to help users compare the performances of the different Workflow
  Managment Systems for their specific needs

## Why is benchmarking important?

The intrinsic generality of the workflow paradigm makes it a powerful abstraction for designing complex applications and executing them on large-scale
distributed infrastructures, such as HPC centres, Grid environments, and Cloud providers. However, such generality becomes an obstacle when evaluating
workflow implementations or Workflow Management Systems (WMSs), as no consistent and commonly agreed key performance metrics exist in the state-of-art
computer science literature.

Instead, different application domains tend to privilege different aspects of the workflow execution process when designing their ideal workflow system.
For example, minimising the control-plane overhead is fundamental when running compute-intensive workflows with billions of fine-grained tasks, while
for data-intensive workflows with few giant steps overlapping computation and communication is far more prominent.

Consequently, different workflow systems excel in handling different kinds of workflows. Still, the lack of community consensus on workflow benchmarking
suites represents a massive obstacle for domain experts trying to compare WMSs based on their needs. Indeed, a direct and fair comparison is possible only
by running multiple state-of-art implementations of the same application on the same execution environment.

Defining several benchmarking suites to evaluate different metrics of interest would represent a crucial improvement for the workflow research
community. Still, benchmarks have no value without building community consensus around them. Conversely, history tells us that highly recognised
benchmarks can tremendously impact research communities, fostering a positive continuous improvement process for years. For example, think about
the role of HPLinpack in the High-Performance Computing community or the ongoing efforts around mastering the training of Deep Neural Networks
(DNNs) on the ImageNet dataset.

## Events and talks


## Related Projects and initiatives

<https://github.com/inutano/cwl-metrics>

<https://elixir-europe.org/internal-projects/commissioned-services/performance-benchmarking> / <https://openebench.bsc.es/dashboard>

<https://github.com/SooLee/Benchmark>

Potential performance reporting formats:

1. [Workflow Trace Archive](https://wta.atlarge-research.com/)
2. [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/)
3. [WfFormat](https://github.com/wfcommons/wfformat)

<!-- Related projects and initiatives related to the  Workflow Benchmarking Group aims: -->


## References

_Articles below are published as [Open Access](https://www.library.manchester.ac.uk/using-the-library/staff/research/open-research/access/),
or with [green open access preprints](https://www.library.manchester.ac.uk/using-the-library/staff/research/open-research/access/understanding/)
where gold open access is not possible. Please [let us know](https://github.com/workflowscommunity/workflowscommunity.github.io/issues) if you are
unable to access any of these publications. To add to this list, please
[suggest a change](https://github.com/workflowscommunity/workflowscommunity.github.io/blob/main/_working_groups/benchmarking.md)._


### Benchmark suites

Elliott Slaughter, Wei Wu, Yuankun Fu, Legend Brandenburg, Nicolai Garcia, Wilhem Kautz, Emily Marx, Kaleb S. Morris, Qinglei Cao, George Bosilca,
Seema Mirchandaney, Wonchan Lee, Sean Treichler, Patrick S. McCormick, Alex Aiken (2020):
[**Task bench: a parameterized benchmark for evaluating parallel runtime performance**](https://doi.org/10.1109/SC41405.2020.00066)
*International Conference for High Performance Computing, Networking, Storage and Analysis (SC)*, **62**, pp. 1-15
<https://doi.org/10.1109/SC41405.2020.00066> ([arXiv:1908.05790]( 	
https://doi.org/10.48550/arXiv.1908.05790))

E. Larsonneur, J. Mercier, N. Wiart, E. L. Floch, O. Delhomme and V. Meyer (2018):
[**Evaluating Workflow Management Systems: A Bioinformatics Use Case**](https://doi.org/10.1109/BIBM.2018.8621141)
*2018 IEEE International Conference on Bioinformatics and Biomedicine (BIBM)*, pp. 2773-2775
<https://doi.org/10.1109/BIBM.2018.8621141> 


### Patterns for scientific workflows

Tainã Coleman, Henri Casanova, Rafael Ferreira da Silva (2021):
[**WfChef: Automated Generation of Accurate Scientific Workflow Generators**](https://doi.org/10.1109/eScience51609.2021.00026)
*17th IEEE EScience Conference*, pp. 159–168
<https://doi.org/10.1109/eScience51609.2021.00026> ([arXiv:2105.00129](
https://doi.org/10.48550/arXiv.2105.00129))

Daniel S. Katz, Andre Merzky, Zhao Zhang, Shantenu Jha (2016):
[**Application skeletons: Construction and use in eScience**](https://doi.org/10.1016/j.future.2015.10.001)
*Future Generation Computer Systems*, **59**, pp. 114-124
<https://doi.org/10.1016/j.future.2015.10.001>

Daniel Garijo, Pinar Alper, Khalid Belhajjame, Óscar Corcho, Yolanda Gil, Carole A. Goble (2014):
[**Common motifs in scientific workflows: An empirical analysis**](https://doi.org/10.1016/j.future.2013.09.018)
*Future Generation Computer Systems*, **36**, pp. 338-351
<https://doi.org/10.1016/j.future.2013.09.018>

Sara Migliorini, Mauro Gambini, Marcello La Rosa, Arthur H.M. ter Hofstede (2011):
[**Pattern-Based Evaluation of Scientific Workflow Management Systems**](https://eprints.qut.edu.au/216123/)
*Unpublished*
<https://eprints.qut.edu.au/216123/>

Ustun Yildiz, Adnene Guabtni, Anne H. H. Ngu (2009):
[**Towards scientific workflow patterns**](https://doi.org/10.1145/1645164.1645177)
*4th Workshop on Workflows in Support of Large-Scale Science (WORKS)*
<https://doi.org/10.1145/1645164.1645177>

Robert Stevens, Carole A. Goble, Patricia G. Baker, Andy Brass (2001):
[**A classification of tasks in bioinformatics**](https://doi.org/10.1093/bioinformatics/17.2.180)
*Bioinformatics*, **17**:1, pp. 180-188
<https://doi.org/10.1093/bioinformatics/17.2.180>


### Performance metrics formats

Rafael Ferreira da Silva (2021):
[**wfcommons/wfformat**](https://doi.org/10.5281/zenodo.4587921)
*Zenodo*
<https://doi.org/10.5281/zenodo.4587921>

L. Versluis, Roland Mathá, Sacheendra Talluri, Tim Hegeman, Radu Prodan, Ewa Deelman, Alexandru Iosup (2020):
[**The Workflow Trace Archive: Open-Access Data From Public and Private Computing Infrastructures**](https://doi.org/10.1109/TPDS.2020.2984821)
*IEEE Transactions on Parallel and Distributed Systems*, **31**:9, pp. 2170-2184
<https://doi.org/10.1109/TPDS.2020.2984821> ([arXiv:1906.07471]( 	
https://doi.org/10.48550/arXiv.1906.07471))

Tazro Ohta, Tomoya Tanjo, Osamu Ogasawara (2019):
[**Accumulating computational resource usage of genomic data analysis workflow
to optimize cloud computing instance selection**](https://doi.org/10.1093/gigascience/giz052).
*GigaScience*, **8**:4, giz052
<https://doi.org/10.1093/gigascience/giz052> ([bioRxiv:456756](https://doi.org/10.1101/456756))

### Workflow benchmarking tools

Tainã Coleman, Henri Casanova, Loïc Pottier, Manav Kaushik, Ewa Deelman, Rafael Ferreira da Silva (2022):
[**WfCommons: A framework for enabling scientific workflow research and development**](https://doi.org/10.1016/j.future.2021.09.043)
*Future Generation Computer Systems*, **128**, pp. 16-27
<https://doi.org/10.1016/j.future.2021.09.043> ([arXiv:2105.14352]( 	
https://doi.org/10.48550/arXiv.2105.14352))

Salvador Capella-Gutierrez, Diana de la Iglesia, Juergen Haas, Analia Lourenco, José María Fernández, Dmitry Repchevsky, Christophe Dessimoz,
Torsten Schwede, Cedric Notredame, Josep Ll Gelpi, Alfonso Valencia (2017):
[**Lessons Learned: Recommendations for Establishing Critical Periodic Scientific Benchmarking**](https://doi.org/10.1101/181677)
*bioRxiv:181677*
<https://doi.org/10.1101/181677> 
