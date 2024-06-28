#!/usr/bin/env python3

######################
# main setup file
########
mymain(){

   #*check python
   echo "-- checking if python is installed";
   #   if (ls python 1> /dev/nul);
   if (which python 1> /dev/null || which python3 1> /dev/null)
   then
	   echo "-- python is installed";
   else
	   echo "-- python is not installed";
	   echo "install python and try again";
	   exit 1
   fi
   i
   # check dependencies
   #checkDependencies

   # check port
   #checkPort

   #check java
   if ( which java 2>/dev/null ); then
       echo "Java available"
   else
       sudo apt update
       sudo apt install fontconfig openjdk-17-jre
       java -version
       openjdk version "17.0.8" 2023-07-18
       OpenJDK Runtime Environment (build 17.0.8+7-Debian-1deb12u1)
       OpenJDK 64-Bit Server VM (build 17.0.8+7-Debian-1deb12u1, mixed mode, sharing)
   fi

   # install jenkins
   if ( which jenkins 2>/dev/null )
   then
       echo "jenkins installed"
   else
       sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
       echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]"
       https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
       sudo apt-get update
       sudo apt-get install jenkins
   fi
}
mymain
