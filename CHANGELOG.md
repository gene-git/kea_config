# Changelog

## [4.3.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-11-05
 - update project version  
 - typo in installer config -> congigs  
 - installer cleanup  
 - update CHANGELOG.md  

## [4.2.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-11-05
 - update project version  
 - Only create /usr/bin/kea-config (no more gen-kea-config)  
 - update CHANGELOG.md  

## [4.1.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-11-05
 - update project version  
 - tidy readme, MIT license, copy dns from gc_dns to keep this standalone  
 - tidy readme, MIT license, copy dns from gc_dns to keep this standalone  
 - tweak installer  
 - tidy do-install  
 - do-install change changelog to CHANGELOG  
 - typo  
 - add README  
 - update CHANGELOG.md  

## [4.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-11-04
 - update project version  
 - Switch to standard python PEP-518  packaging  

## [3.1] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-22
 - Remove local class_dns file  
 - update changelog  
 - Remove local dns class and use GcDns class from gc_utils module  
 - update do-install to handle filename change Changelog.md  
 - update changelog  

## [3.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-19
 - Skip HA when only primary  
 - add phone  
 - fix more silly  
 - normalize incoming dst  
 - remove duplicate // in link  
 - Missing makedir in do-install  
 - typo  
 - add link in /usr/bin/gc-kea-config for convenience  
 - fix do-install config dir  
 - typo in changelog  

## [2.2] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-06-09
 - Changelog  
 - Add license  
 - add configs dir  
 - Install script for package build  

## [2.1] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-06-09
 - lint picking  

## [2.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-06-08
 - Rewrite with classes  
 - fix typo in agent. Turn off pdb  

## [1.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-03-04
 - Tidy more - move config extract to classes file  
 - renamed sameple config  
 - Add conreol agent  
   output now in configurable directory  
   split single python file into smaller components;  
   ;  
 - tidy  
 - Better control over file names etc  
 - error handling for dns lookups  
 - Initial commit - generate kea-dhcp4 server configs  

