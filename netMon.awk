
BEGIN {FS = " "; RS = "\n"}

FNR==NR{
   if ($2 == "RRDIPT_INPUT")
		printOut = 0
   if (printOut == 1)
   {
   		if ($1 > 0 && $1 != "pkts") {
   		#   pkt, byte, source, destination
		#	print $1,$2,$8,$9
			if ($8 != "0.0.0.0/0")
			{
				dataOut[$8] = $2
                # Since we have a dataOut variable, we should set our dataIn
                # variable to 0, (in case we have no dataIn) unless it is already set
                if (dataIn[$8]=="")
                {
                    dataIn[$8] = 0
                }
		 
			}
			else if($9 != "0.0.0.0/0")
			{
				dataIn[$9] = $2
			}
		}
   }
   if ($2 == "RRDIPT_FORWARD")
	printOut = 1
	next
}
# Now we read the second file;  contains our arp <> IP connections
{
	mac[$1] = $4
}


END {
	for (x in dataOut)
	{
		print mac[x]","dataOut[x]","dataIn[x]	
	}
}
