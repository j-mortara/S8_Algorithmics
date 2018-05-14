all:
	echo "#!/bin/sh" > algo.ex
	echo "python3 source/exemples.py \$$@" >> algo.ex
	echo "#!/bin/sh" > stat.ex
	echo "python3 source/generator.py \$$@" >> stat.ex
	chmod +x *.ex

clean:
	rm *.ex

