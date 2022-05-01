all:
	../../g2labs-message-generator.py simple_messages.g2msg
	gcc -I. -o simple_test simple_message.c simple_test.c

clean:
	rm -rf simple_test