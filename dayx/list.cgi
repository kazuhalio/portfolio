#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DAY COUNTER-EX : list.cgi - 2023/07/08
#│ copyright (c) KentWeb, 1997-2023
#│ https://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 設定ファイル取込
require './init.cgi';
my %cf = set_init();

# リスト一覧
list_data();

#-----------------------------------------------------------
#  リスト一覧
#-----------------------------------------------------------
sub list_data {
	# 累計ファイル読み込み
	open(IN,"$cf{logfile}") or die "open err: $!";
	my $data = <IN>;
	close(IN);
	
	my ($day) = (split(/<>/,$data))[0];
	
	# 本日ファイル読み込み
	open(IN,"$cf{todfile}") or die "open err: $!";
	my $tod = <IN>;
	close(IN);
	
	# 時間取得
	$ENV{TZ} = "JST-9";
	my ($mday,$mon,$year,$wday) = (localtime(time))[3..6];
	my @week = ('日','月','火','水','木','金','土');
	my $date = sprintf("%02d/%02d (%s) ",$mon+1,$mday,$week[$wday]);
	my $this_mon  = sprintf("%04d/%02d",$year+1900,$mon+1);
	
	# 日次ファイル読み込み
	my ($dcount,$dcateg);
	open(IN,"$cf{dayfile}") or die "open err: $!";
	while(<IN>) {
		my ($date,$cnt) = split(/<>/);
		
		$dcount .= "$cnt,";
		$dcateg .= "'$date',";
	}
	close(IN);
	
	$dcount =~ s/,$//;
	$dcateg =~ s/,$//;
	
	# 月次ファイル読み込み
	my ($mcount,$mcateg);
	open(IN,"$cf{monfile}") or die "open err: $!";
	while(<IN>) {
		my ($date,$cnt) = split(/<>/);
		
		$mcount .= "$cnt,";
		$mcateg .= "'$date',";
	}
	close(IN);
	
	$mcount =~ s/,$//;
	$mcateg =~ s/,$//;
	
	# テンプレート読み込み
	open(IN,"$cf{tmpldir}/list.html") or die "open err: $!";
	my $tmpl = join('',<IN>);
	close(IN);
	
	$tmpl =~ s/!list_title!/$cf{list_title}/g;
	$tmpl =~ s/!this_month!/$this_mon/g;
	$tmpl =~ s/!day_count!/$dcount/g;
	$tmpl =~ s/!day_categ!/$dcateg/g;
	$tmpl =~ s/!mon_count!/$mcount/g;
	$tmpl =~ s/!mon_categ!/$mcateg/g;
	
	# 表示開始
	print "Content-type: text/html; charset=utf-8\n\n";
	footer($tmpl);
}

#-----------------------------------------------------------
#  月の末日
#-----------------------------------------------------------
sub last_day {
	my ($year,$mon) = @_;
	
	my $last = (31,28,31,30,31,30,31,31,30,31,30,31)[$mon - 1]
		+ ($mon == 2 && (($year % 4 == 0 && $year % 100 != 0) || $year % 400 == 0));
	
	return $last;
}

#-----------------------------------------------------------
#  桁区きり
#-----------------------------------------------------------
sub comma {
	local($_) = @_;
	
	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	$_;
}

#-----------------------------------------------------------
#  フッター
#-----------------------------------------------------------
sub footer {
	my $foot = shift;
	
	# 著作権表記（削除禁止）
	my $copy = <<EOM;
<p style="margin-top:2em;text-align:center;font-family:Verdana,Helvetica,Arial;font-size:10px;">
	- <a href="https://www.kent-web.com/" target="_top">DayCounterEX</a> -
</p>
EOM

	if ($foot =~ /(.+)(<\/body[^>]*>.*)/si) {
		print "$1$copy$2\n";
	} else {
		print "$foot$copy\n";
		print "</body></html>\n";
	}
	exit;
}

