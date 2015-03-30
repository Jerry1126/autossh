#!/usr/bin/perl

$file = shift(@ARGV);
$regex = shift(@ARGV);

if(-e $file){
  open (MyFile, $file);
  local $/ = undef;
  my $content=<MyFile>;
  if(defined($regex)){
    if($content =~ m/$regex/smio){
      print 1;
    }
    else{
      print "There is no such content in file";
    }
  }
  else{
    print 1
  }
}
else
{
print "No Such File";
}
