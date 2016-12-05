Setup for Neuroimaging on JHPCE Cluster
==========

First off, you should highly consider a Unix-like system.  [Cygwin](https://www.cygwin.com/) alongside [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/) may work well, but I haven't tested it, don't have answers, and don't want to be the person you come to for questions.

Let's begin by locating your `.bash_profile`, which should be located at `~/.bash_profile`.  You can edit using `vi`.  

If you use `vi`, to insert something just type `i` and then copy and paste the code and then to write the file and quit, type `ESC+:+wq`.  The `ESC` escapes anything you were doing (like inserting text), the `w` means write the file, and `q` means quit.  If you edited a file and don't want to save changes, use `:q!`.  

I don't use `vi` and recommend [`Sublime Text`](http://www.sublimetext.com/), and setting it up to [edit files locally](http://www.danieldemmel.me/blog/2012/09/02/setting-up-rmate-with-sublime-text-for-remote-file-editing-over-ssh/), and another link [here](http://pogidude.com/2013/how-to-edit-a-remote-file-over-ssh-using-sublime-text-and-rmate/).  Make an [alias]() in your `~/.bash_profile` by adding the content:
```{r, engine='bash'}
alias subl="rmate -p MYPORTHERE"
```
where `MYPORTHERE` is a number that you set (that hopefully doesn't conflict with others).  Then you can do `subl filename.ext` while you are on JHPCE (**not a node**) and the file will open on your local machine.

## FSL Installation

We will first add [FSL](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/) to your `~/.bash_profile`, so you can use functions.

```{r, engine='bash', eval=FALSE}
# FSL Configuration
FSLDIR=/legacy/dexter/disk2/smart/programs/local/fsl
PATH=${FSLDIR}/bin:${PATH}
source ${FSLDIR}/etc/fslconf/fsl.sh
. ${FSLDIR}/etc/fslconf/fsl.sh
export FSLDIR PATH
```

## ANTsR

You can install [Install ANTsR from GitHub](http://stnava.github.io/ANTsR/), which I recommend.  But if you want to get started with ANTsR right now (and download the GitHub later), you can use the following command in `R`:

```{r, eval=FALSE}
.libPaths( c( .libPaths(), "/legacy/dexter/disk2/smart/programs/R_Packages") )
```

[CMake](http://www.cmake.org/) is required for an install of ANTsR, so put this in your `~/.bash_profile`:

```{r, engine='bash', eval=FALSE}
export PATH=${PATH}:/legacy/dexter/disk2/smart/programs/cmake-2.8.12.2
```
and then you can install ANTsR using:
```{r antsr,eval=FALSE}
devtools::install_github("stnava/cmaker") 
devtools::install_github("stnava/ITKR") 
devtools::install_github("stnava/ANTsR") # ANTsR - this takes a LONG time to run
```

## ANTs

To run the general suite of ANTs, put this in your `~/.bash_profile`:

```{r, engine='bash', eval=FALSE}
export PATH=${PATH}:/legacy/dexter/disk2/smart/programs/ANTs.2.1.0.Debian-Ubuntu_X64
```


## AFNI
If you would like to use commands from [AFNI (Analysis of Functional NeuroImages)](http://afni.nimh.nih.gov/afni/), then you need to add the path to AFNI to the `PATH` environmental variable.  Simply put, add this to `~/.bash_profile`:
```{r, engine='bash', eval=FALSE}
export PATH=${PATH}:/legacy/dexter/disk2/smart/programs/afni
```

## R packages

```{r packages,eval=FALSE}
install.packages("oro.dicom") # working with DICOM images
install.packages("oro.nifti") # working with NIfTI objects 
install.packages("devtools") # Getting GitHub Packages
devtools::install_github("muschellij2/fslr") # up-to-date fslr package
# install.packages("fslr") # Package for interfacing FSL - CRAN version
# devtools::install_github("stnava/ANTsR") # ANTsR - this takes a LONG time to run
devtools::install_github("muschellij2/extrantsr") # EXTRA ANTsR functionality
```

## MATLAB

In your `~/.bashrc`, put the command:

```{r, engine='bash', eval=FALSE}
module load matlab
```

## DCM2NII

To use [`dcm2niix`](https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage#General_Usage), a DICOM to NIfTI converter, put this in your `~/.bash_profile`:

```{r, engine='bash', eval=FALSE}
export PATH=${PATH}:/legacy/dexter/disk2/smart/programs/dcm2niix/console/ 
```

## FreeSurfer

To use [FreeSurfer](http://freesurfer.net/), add the following to the `~/.bash_profile`:

```{r, engine='bash', eval=FALSE}
export FREESURFER_HOME=/legacy/dexter/disk2/smart/programs/freesurfer
source ${FREESURFER_HOME}/SetUpFreeSurfer.sh
```


## Camino

To use [Camino](http://camino.cs.ucl.ac.uk//), add the following to the `~/.bash_profile`:

```{r, engine='bash', eval=FALSE}
export PATH=${PATH}:/legacy/dexter/disk2/smart/programs/camino/bin
```

# Cluster Organization

## Structure of MSMRI 
```
Data (Organized by Source)
    - NIH
    - Hopkins

Projects
    - OASIS
        - Processed_Data
            - scripts
        - sandbox
            - scripts
            - results
        - Manuscript
            - scripts 
            - results
        - ReadME.txt
    - SuBLIME
    - QMRI
```

## Example ReadME.txt

```
Owner:
Email:
Source:
Description:
URL (if applicable):
Users:
```
