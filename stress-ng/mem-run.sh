# vim: set et tw=4 sw=4
#!/bin/bash

if [ "$#" != 1 ]; then
    echo "No arguments specified.";
    exit 1;
fi

opt=$1

case $opt in
    "memory")
        echo "##### Executing memory stressors";
        let "workers=60 + $RANDOM % 30";

        # Add some memory workers that do no release memory
        command="/usr/bin/stress-ng --vm $workers --vm-bytes 2G --vm-hang 0";
        echo $command;
        ( $command; )&

        while true; do
            let "time_out=(60 + $RANDOM%120)";
            command_var="/usr/bin/stress-ng --sequential 1 --class vm
                                            --timeout $time_out";

            let "workers_const_incr=40 + $RANDOM % 30";
            # At each iteration spawns vm-workers that do not release memory
            # Simulates a scenario similar to memory leak
            command_inc="/usr/bin/stress-ng --vm workers_const_incr
                                            --vm-bytes 500m --vm-hang 0";
            # command_var adds some randomness in memory usage by stressing
            # the "vm" class in stress-ng
            `$command_var`;
            ($command_inc)&
        done;
        ;;

    "cpu")
        echo "#### Executing CPU stressors";
        while true; do
            let "workers=5 + $RANDOM % 5";
            let "cpu_load=20 + $RANDOM % 20";
            let "load_slice=3000 + $RANDOM % 2000";
            let "time=$RANDOM % 15";
            command="/usr/bin/stress-ng --cpu $workers --cpu-load $cpu_load
                                            --cpu-load-slice $load_slice -t "$time"m";
            echo "Executing $command";
            $command;
        done;
        ;;

    "io")
        echo "#### Executing I/O stressors";
        let "aio_workers=1 + $RANDOM % 4"

        # Add some asynchronous io calls. From experiments they do not exercise
        # significant cpu.
        command_const="/usr/bin/stress-ng --aio $aio_workers";
        echo "Executing $command_const";
        ( $command_const; )&

        while true; do
            # Keeping only upto 3 workers for hdd and utime as they seem to
            # exercise cpu significantly
            let "hdd_workers=$RANDOM % 3";
            let "utime_workers=$RANDOM % 3";
            let "timeout=$RANDOM % 10";

            command_var="/usr/bin/stress-ng --hdd $hdd_workers
                                            --utime $utime_workers --utime-fsync
                                            -t "$timeout"m";

            echo "Executing $command_var";
            $command_var;
            let "sleep_time=20 + $RANDOM % 160";
            "`sleep $sleep_time`";
        done;
        ;;
esac
