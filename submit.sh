#!/usr/bin/env bash

# Main driver to submit jobs 
# Author Ryuta Kiuchi <kiuchi@ihep.ac.cn> and Konglingteng <konglingteng15@mails.ucas.ac.cn>
# Created [2018-06-16 Sat 16:00] 

usage() {
	printf "NAME\n\tsubmit.sh - Main driver to submit jobs\n"
	printf "\nSYNOPSIS\n"
	printf "\n\t%-5s\n" "./submit.sh [OPTION]" 
	printf "\n\start event_sel in 1.1.6 1.2.7 1.3.7\n" 
	printf "\nOPTIONS\n" 
        printf "\n\t%-9s  %-40s"  "1"      "[Run HZZ channel]"
        printf "\n\t%-9s  %-40s"  "2"      "[Run ZH channel]"
        printf "\n\n"
	printf "\nDATE\n"
	printf "\n\t%-5s\n" "Janurary 2021" 
}

usage_1() {
        printf "\n"
        printf "\n\t%-9s  %-40s"  "1.1"      "[HZZ SM channel]"
        printf "\n\t%-9s  %-40s"  "1.2"      "[HZZ CP odd channel]"
        printf "\n\t%-9s  %-40s"  "1.3"      "[HZZ BSM CP even channel]"
        printf "\n\t%-9s  %-40s"  "1.4"      "[BDT classification]"
}

usage_2() {
        printf "\n"
        printf "\n\t%-9s  %-40s"  "2.1"      "[ZH SM channel]"
        printf "\n\t%-9s  %-40s"  "2.2"      "[ZH CP odd channel]"
        printf "\n\t%-9s  %-40s"  "2.3"      "[ZH BSM CP even channel]"
        printf "\n\t%-9s  %-40s"  "2.4"      "[BDT classification]"
}

usage_1_1() {
        printf "\n"
        printf "\n\t%-9s  %-40s"  "1.1.1"      "[Please run the JHU generator and name the output as 'outfile_HZZ_SM.lhe' ]"
        printf "\n\t%-9s  %-40s"  "1.1.2"      "[Compile the root conversion script]"
        printf "\n\t%-9s  %-40s"  "1.1.3"      "[Convert lhe file into root file]"
}


usage_1_2() { 
	printf "\n" 
        printf "\n\t%-9s  %-40s"  "1.2.1"      "[Please run the JHU generator and name the output as 'outfile_HZZ_CPodd.lhe' ]"
        printf "\n\t%-9s  %-40s"  "1.2.2"      "[Compile the root conversion script]"
        printf "\n\t%-9s  %-40s"  "1.2.3"      "[Convert lhe file into root file]"
}

usage_1_3() {  
        printf "\n" 
        printf "\n\t%-9s  %-40s"  "1.3.1"      "[Please run the JHU generator and name the output as 'outfile_HZZ_BSM_CPeven.lhe' ]"
        printf "\n\t%-9s  %-40s"  "1.3.2"      "[Compile the root conversion script]"
        printf "\n\t%-9s  %-40s"  "1.3.3"      "[Convert lhe file into root file]"
}

usage_2_1() {
        printf "\n"
        printf "\n\t%-9s  %-40s"  "2.1.1"      "[Please run the JHU generator and name the output as 'outfile_ZH_SM.lhe' ]"
        printf "\n\t%-9s  %-40s"  "2.1.2"      "[Compile the root conversion script]"
        printf "\n\t%-9s  %-40s"  "2.1.3"      "[Convert lhe file into root file]"
}

usage_2_2() {
        printf "\n"
        printf "\n\t%-9s  %-40s"  "2.2.1"      "[Please run the JHU generator and name the output as 'outfile_ZH_CPodd.lhe' ]"
        printf "\n\t%-9s  %-40s"  "2.2.2"      "[Compile the root conversion script]"
        printf "\n\t%-9s  %-40s"  "2.2.3"      "[Convert lhe file into root file]"
}

usage_2_3() {
        printf "\n"
        printf "\n\t%-9s  %-40s"  "2.3.1"      "[Please run the JHU generator and name the output as 'outfile_HZZ_BSM_CPeven.lhe' ]"
        printf "\n\t%-9s  %-40s"  "2.3.2"      "[Compile the root conversion script]"
        printf "\n\t%-9s  %-40s"  "2.3.3"      "[Convert lhe file into root file]"
}

if [[ $# -eq 0 ]]; then
    usage
    echo "Please enter your option: "
    read option
else
    option=$1    
fi

signal_slcio_dir_ll=/cefs/data/DstData/CEPC240/CEPC_v4/higgs/E240.Pe2e2h_zz.e0.p0.whizard195

signal_slcio_dir_nn=/cefs/data/DstData/CEPC240/CEPC_v4/higgs/E240.Pnnh_zz.e0.p0.whizard195

signal_slcio_dir_qq=/cefs/data/DstData/CEPC240/CEPC_v4/higgs/E240.Pqqh_zz.e0.p0.whizard195

signal_HZZ=outfile_HZZ_SM.root

bkg_HZZ=outfile_HZZ_BSM_CPeven.root

    # --------------------------------------------------------------------------
    #  1.1 HZZ SM channel   
    # --------------------------------------------------------------------------

sub_1_1(){
case $option in 

    1.1) echo "run standard model channel..."
         ;;

    1.1.1) echo "Please prepare outfile_HZZ_SM.lhe"

    1.1.2) echo "Compiling root conversion script"
           c++ -o lhe_conversion_HZZ `root-config --glibs --cflags` -lm lhe_conversion_HZZ.cpp
           ;;

    1.1.3) echo "Root tree generation"
           ./lhe_conversion_HZZ outfile_HZZ_SM.lhe
           mv trial_HZZ.root outfile_HZZ_SM.root
           ;;

    esac
}

    # --------------------------------------------------------------------------
    #  1.2 HZZ CP odd channel   
    # --------------------------------------------------------------------------

sub_1_2(){
case $option in 

    1.2) echo "Run CP odd channel..."
         ;;
    1.2.1) echo "Please prepare outfile_HZZ_CPodd.lhe"

    1.2.2) echo "Compiling root conversion script"
           c++ -o lhe_conversion_HZZ `root-config --glibs --cflags` -lm lhe_conversion_HZZ.cpp
           ;;

    1.2.3) echo "Root tree generation"
           ./lhe_conversion_HZZ outfile_HZZ_CPodd.lhe
           mv trial_HZZ.root outfile_HZZ_CPodd.root
           ;;

    esac
}

    # --------------------------------------------------------------------------
    #  1.3 HZZ BSM CP even channel
    # --------------------------------------------------------------------------

sub_1_3(){
case $option in 

    1.3) echo "Run BSM CP even channel..."
         ;;
    1.3.1) echo "Please prepare outfile_HZZ_BSM_CPeven.lhe"

    1.3.2) echo "Compiling root conversion script"
           c++ -o lhe_conversion_HZZ `root-config --glibs --cflags` -lm lhe_conversion_HZZ.cpp
           ;;

    1.3.3) echo "Root tree generation"
           ./lhe_conversion_HZZ outfile_HZZ_BSM_CPeven.lhe
           mv trial_HZZ.root outfile_HZZ_BSM_CPeven.root
           ;;

    esac
}

    # --------------------------------------------------------------------------
    #  1.4 BDT classification  
    # --------------------------------------------------------------------------

sub_1_4(){
case $option in 

    1.4) echo "BDT classifications for given channel"
         ;;

    1.4.1) echo  "BDT classification"
           python3 train_model.py ${signal_HZZ} ${bkg_HZZ} 
           ;; 
    esac
}

sub_2_1(){
case $option in
  esac

}

sub_2_2(){
case $option in
    esac
}

sub_2_3(){
case $option in
    esac
}

sub_2_4(){
case $option in
    esac
}

sub_1(){
case $option in 
# sample: 1.1 is print detail information about each step and then you can run the step you want.
#         1.1.* is directly running the step. 
    # --------------------------------------------------------------------------
    #  Data  
    # --------------------------------------------------------------------------

    1.1) echo "run SM sample"
        usage_1_1
        echo "Please enter your option: " 
        read option 
        sub_1_1 option 
        ;;
    1.1.*) echo "run SM sample"
        sub_1_1 option
        ;;
        
    1.2) echo "run CP odd sample"
        usage_1_2
        echo "Please enter your option: " 
        read option  
        sub_1_2 option 
        ;;
    1.2.*) echo "run CP odd sample"
        sub_1_2 option 
        ;;

    1.3) echo "run BSM CP even sample." 
        usage_1_3
        echo "Please enter your option: " 
        read option 
        sub_1_3 option 
        ;;
    1.3.*) echo "run BSM CP even sample"
        sub_1_3 option 
        ;;

    1.4) echo "BDT classification"
        usage_1_4
        echo "Please enter your option: " 
        read option
        sub_1_4 option 
        ;;        
    1.4.*) echo "BDT classification"
        sub_1_4 option 
        ;; 
esac
}

sub_2(){
case $option in

    2.1) echo "run SM sample"
        usage_2_1
        echo "Please enter your option: " 
        read option
        sub_2_1 option
        ;;
    2.1.*) echo "run SM sample"
        sub_2_1 option
        ;;

    2.2) echo "run CP odd sample"
        usage_2_2
        echo "Please enter your option: " 
        read option
        sub_2_2 option
        ;;
    2.2.*) echo "run CP odd sample"
        sub_2_2 option
        ;;

    2.3) echo "run BSM CP even sample." 
        usage_2_3
        echo "Please enter your option: " 
        read option
        sub_2_3 option
        ;;
    2.3.*) echo "run BSM CP even sample"
        sub_2_3 option
        ;;

    2.4) echo "BDT classification"
        usage_2_4
        echo "Please enter your option: " 
        read option
        sub_2_4 option
        ;;
    2.4.*) echo "BDT classification"
        sub_2_4 option
        ;;
esac
}

case $option in
    1) echo "run HZZ"
       usage_1
       echo "Please enter your option: "
       read option
       sub_1 option
        ;;
    1.*) echo "run HZZ"
       sub_1 option
        ;;

    2) echo "run ZH"
       usage_2
       echo "Please enter your option: "
       read option
       sub_2 option
        ;;
    2.*) echo "run ZH"
       sub_2 option
        ;;

esac
