#!/usr/bin/perl -w
# filter_bin_file
#use strict 
use Getopt::Long;
use File::Basename;

my $script = basename $0;
my $input_file = '';
my $output_file = '';
my $output_file_alt = ''; 

my $ON_WINDOWS = 0;
   $ON_WINDOWS = 1 if ($^O =~ /^MSWin/) or ($^O eq "Windows_NT");
if ($ON_WINDOWS and $ENV{'SHELL'}) {
    if ($ENV{'SHELL'} =~ m{^/}) {
        $ON_WINDOWS = 0;  # make Cygwin look like Unix
    } else {
        $ON_WINDOWS = 1;  # MKS defines $SHELL but still acts like Windows
    }
}

my $NN     = chr(27) . "[0m";  # normal
   $NN     = "" if $ON_WINDOWS or !(-t STDERR); # -t STDERR:  is it a terminal?
my $BB     = chr(27) . "[1m";  # bold
   $BB     = "" if $ON_WINDOWS or !(-t STDERR);
my $usage = "
  ${BB}Usage:${NN}
    $script [options] <input_bin_file> <output_bin_file>  [<output_bin_file2> if --two_mono]

  ${BB}Brief Description:${NN}
    Filter a binary file to remove markers

  ${BB}Options:${NN}
    --bytes-to-read=<bits>   This tells how many bytes of data are to be read in a word.
                             Default is '2'

    --marker-to-remove=<marker_word>   This is the marker to remove.
                             Default is '0x8000'

    --reverse-endian         Reverse the endian from the input.
                             Default is 'No'
							 
    --two_mono               if the input is two mono 

    --help                   Help

";

my (
	$bytes_to_read     ,
  $remove_marker     ,
  $rev_end           ,
  $input_two_mono    ,  
  
) = '';

my @files = ();

die $usage unless GetOptions (
	'bytes-to-read=i'                 => \$bytes_to_read     , 
	'marker-to-remove=i'              => \$remove_marker     ,
	'reverse-endian'                  => \$rev_end           ,
	'two_mono'                        => \$input_two_mono    , 
	'help'                            => sub {print $usage;exit},
	'<>'                              => \&inp_file_save
);

sub inp_file_save {
	push(@files, $_[0]);
}

$bytes_to_read  = ($bytes_to_read)  ? $bytes_to_read  : 2          ;
$remove_marker  = ($remove_marker)  ? $remove_marker  : 0x8000       ;
$input_two_mono  = ($input_two_mono)  ? $input_two_mono  : 0       ;

# Setting the character read size
$/ = \$bytes_to_read;

if ($input_two_mono) {
die "ERROR: Please enter input_file_name and output_file_name(L),output_file_name(R) :",scalar @files, " $files[0] , $files[1], $files[2]!!!!\n" unless ((scalar @files) == 3);
} else {
die "ERROR: Please enter input_file_name and output_file_name :",scalar @files, " $files[0] , $files[1] !!!!\n" unless ((scalar @files) == 2);
}

$input_file = $files[0];
$output_file = $files[1];

if ($input_two_mono) {
$output_file_alt =  $files[2];
}


open(FH, "<$input_file") or die "ERROR: cannot open the input file: $input_file !!!\n";
binmode(FH);

open(FOH, ">$output_file") or die "ERROR: cannot open the output file: $output_file !!!\n";
binmode(FOH);


if ($input_two_mono){
open(FOH2, ">$output_file_alt") or die "ERROR: cannot open the output file: $output_file_alt !!!\n";
binmode(FOH2);

}



my $in = 0;
my @out = ();
my $pingpong = 0;
 


while (read(FH, $in, 2)) {
	@out = unpack("(H2)$bytes_to_read",$in);
	if ($rev_end) {
		$hex_num = join "", reverse @out;
	} else {
		$hex_num = join "", @out;
	}
	
  if ($input_two_mono){
      if ($pingpong) {
	     $pingpong  = 0;  
	  } else  {
	     $pingpong  = 1;
	  }
	  if ($pingpong) {
		  if (hex($hex_num) != $remove_marker) {
			print FOH $in;  #LEFT CH 
		  } 
	  } else {
	  	  if (hex($hex_num) != $remove_marker) {
			print FOH2 $in; #RIGHT
		  } 
	  }
  } else {
  
		if (hex($hex_num) != $remove_marker) {
		print FOH $in;
	  }
  }

}

close(FH);
close(FOH);
if ($input_two_mono){
close(FOH2);
}

