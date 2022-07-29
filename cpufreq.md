# CPU Frequency Scaling

	apt install cpufrequtils

## Information

	ondemand governor

	root@pinenote:~# cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
	408000 600000 816000 1104000 1416000 1608000 1800000


* 816 MHz:

	cpufreq-set -u 816000; cpufreq-set -u 816000; cpufreq-info

* 1.10 GHz:

	cpufreq-set -u 1104000; cpufreq-set -d 1104000 ; cpufreq-info

  Better use?:

	cpufreq-set -u 1104000; cpufreq-set -d 816000 ; cpufreq-info

* 1.61 GHz:

	cpufreq-set -u 1608000; cpufreq-set -u 1608000; cpufreq-info

* 1.8 Ghz:

	cpufreq-set -u 1800000; cpufreq-set -d 1800000 ; cpufreq-info

## TODO

* Check with other governors, maybe there is one that yields good performance

