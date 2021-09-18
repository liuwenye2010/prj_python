#!/bin/sh
#KeyEvent: KEYCODE_POWER:22; KEYCODE_SLEEP:223; KEYCODE_WAKEUP:224
# Returns the power state of the screen 1 = on, 0 = off
count=0
for((i=1;i<=5;i++)); 
do
	echo $i
	sleep 15
	getDisplayState() {
		state=$(adb -s $1 shell dumpsys power | grep mScreenOn= | grep -oE '(true|false)')
		echo -e "\nstate check: $state"

		# If we didn't get anything it might be a pre-lollipop device
		if [ "$state" = "" ]; then
			state=$(adb -s $1 shell dumpsys power | grep 'Display Power' | grep -oE '(ON|OFF)')
			#state=$(adb shell dumpsys input_method | grep -c "mScreenOn=true")
		fi

		if [ "$state" = "ON" ] || [ "$state" = "true" ]; then
			return 1;
		else
			return 0;
		fi
	}
	echo "Turning off screen when wake up"
	for device in `adb devices | grep device$ | cut -f1`
	do
		echo -n "Found device: $device ... "

		getDisplayState $device
		
		state=$?
		echo "current screen state value is: $state"
		echo "the power state of the screen 1 = on, 0 = off"

		# If wake up turn off the screen
		if [ $state -eq 0 ]; then
            count=$((${count} + 1))
			echo "not wake up" $count "times"
	
		else
			echo "the screen is on then turning off"
			adb -s $device shell input keyevent KEYCODE_POWER
		fi

	done
done
exec /bin/bash
