#!/usr/bin/perl


#!/usr/bin/perl
use warnings;
use strict;
use List::Util qw[min max];
use Time::HiRes qw[sleep];

# read IBM 6094-010 lights

my $DEFPORT = "/dev/serial/by-id/usb-Silicon_Labs_IBM-LPFK_75BB67F3-A9AA8F7A-if00-port0";
my $PORT = ($::ENV{'LIGHTS_PORT'} || $DEFPORT);

print "Opening $PORT...\n";
my $FH;
open($FH, "+> $PORT") || die $!;
my $bits = "cs8 parenb parodd -istrip";
system("stty -F $PORT raw clocal  9600 -crtscts $bits  -hupcl ignbrk ignpar -onlcr -iexten -echo -echoe -echok -echoctl -echoke");
binmode $FH;
select((select($FH), $|=1)[0]);

my $v = read_nb(1);
print "Junk in port: ".safe($v)."\n" if $v;

# reset device
write_dat("\x01");
sleep(0.8);

#check ID
write_dat("\x06");
$v = read_nb(1, 1);

unless ($v eq "\x03") {
  die "Lights are not attached: got ".safe($v)."\n";
};

print "Lights detected\n";

#read_dials_pos();

# output lights
my @lights = map { 0 } (0..31);

write_dat("\x08"); # enable output
update_lights();

while (1) {
  my $cmd = read_nb(10.0, 1);
  if ($cmd eq '') {
    print "! Idle\n";
    next;
  };
  my $btn = ord($cmd);
  if ($btn == 0x80) {
    # incorrect lights command
    print "Incorrect lights. re-doing\n";
    send_lights();
    next;
  };

  if (($btn < 0) or ($btn > 31) or (length($cmd) != 1)) {
    print("Strange data received: ".safe($cmd)."\n");
  };

  # buttons 0-3 are muliple choice (unless pressed twice), rest are toggle
  my $lc4 = ($lights[0] + $lights[1] + $lights[2] + $lights[3]);
  if ($btn <= 3) {
    if ((($btn == 3) || ($btn == 0)) &&
         ($lc4 == 1) && ($lights[$btn])) {
       $lights[0] = $lights[1] = $lights[2] = $lights[3] = ($btn == 0)?0:1; 
       $lights[$btn] ^= 1;
    }
#    elsif ($lc4) {
#       $lights[0] = $lights[1] = $lights[2] = $lights[3] = 0; 
#    };
  }; 

  $lights[$btn] ^= 1;
  printf("Button %d pressed, light set to %d\n", $btn, $lights[$btn]);
  update_lights();
};


sub update_lights {
  $v = "\x00\x00\x00\x00";
  for my $x (0..31) {
    vec($v, $x ^ 7, 1) = 1 if $lights[$x];
  };
  write_dat("\x94$v");
  my $r = read_nb(0.1, 1);
  warn "Set LIGHTS failed\n" if ($r ne "\x81");
};



# commands (at 9600 8-O-1):
#   \01           reset device
#   \06           query ID, returns \08
#   \08           enable data sending from keys
#   \09           disable data sending from keys
#   \0E           enter echo mode (until \01 or \0F, ignores rest)
#   \94           set light status


############################

sub read_nb {
  my ($timeout,$maxlen) = @_;
  my $rin = '';
  my $result = '';
  $maxlen ||= 8;
  vec($rin, fileno($FH), 1) = 1;
  while (select($rin, undef, undef, $timeout) != 0) {
    my $buf = '';
    $!=0;
    my $rv = sysread($FH, $buf, min(1024, $maxlen - length($result)));
    if ($rv <= 0) {
      die "Error while reading from port: $!\n";
    };
    $result .= $buf;
    last if length($result) >= $maxlen;
  };
  if ($result) {
    #print $LOGF "r ".safe($result)."\n";
    ;
  };
  return $result;
};

sub write_dat {
  my ($msg) = @_;
  #print $LOGF "w ".safe($msg)."\n";
  if (syswrite($FH, $msg) != length($msg)) {
    die "syswrite failed\n";
  };
};


sub safe {
  my ($r) = @_;
  $r =~ s/([^\x20-\x5B\x5D-\x7F])/sprintf("\\%.2X", ord($1))/ge;
  return $r;
};

sub desafe {
  my ($r) = @_;
  $r =~ s[\\([0-9A-F][0-9A-F])][chr(eval("0x$1"))]ge;
  return $r;
};
