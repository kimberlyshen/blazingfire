#!/usr/local/bin/perl
use strict;
use warnings;
use Net::Ping;

import os;

use English qw(-no_match_vars);
local $OUTPUT_AUTOFLUSH = 1;

my $name = "netstat -rn \| tee out.txt >/dev/null";
my $devices = "grep \"..:..:..:..:..:..\" out.txt \| tee devices.txt >/dev/null";

system($name);
system($devices);

print "Output done \n ";

open FILE, "devices.txt" or die $!;

my @words;
my $ip_count = 0;
my $mac_count = 0;
my @ip;
my @mac;

while (<FILE>)
{
    
    chomp;
    print "$_\n";
    
    
    # my $devices = $_;
    #   system("ping $_");
    
    @words = split(' ');
    
    my $id = 0;
    
       foreach my $word (@words) {
           if( $id < 2 ){
               print "printin word\n";
               print "$word\n";
               
               
               if( $word =~ /[0-9][0-9][0-9]\.[0-9][0-9][0-9]\.[0-9][0-9]\./ ){
                   print "It's an IP address\n";
                   $ip[$ip_count] = $word;
                   $ip_count++;
               }
               
               if ( $word =~ /..:..:..:..:..:../ ){
                   print "It's a Mac Address\n";
                   $mac[$mac_count] = $word;
                   $mac_count++;
               }
           }
           $id++;
       }
    $id = 0;
}

##print "THE HELL\n";

##print "@ip\n";
##print "@mac\n";
my $host;
my $p;

my $count = 0;
my $numDevices = 0; 



for($count = 0; $count < $ip_count; $count++){
    
    if( $ip[$count] =~ /[0-9][0-9][0-9]\.[0-9][0-9][0-9]\.[0-9][0-9]\./ ){
         print "$ip[$count]\n";
        
               $host = $ip[$count];
          my $timeout = 10;
        
        $p = Net::Ping->new("icmp");
        
        if( $p->ping($host, $timeout) ){
            print "Host ".$host." is alive\n";
			$numDevices++; 
        }
        else {
            #print "Warning: ".$host." appears to be down or icmp packets are blocked by their server\n";
        }
        
        
    }
}

print $numDevices; 
#print "\n"

close FILE or die $!