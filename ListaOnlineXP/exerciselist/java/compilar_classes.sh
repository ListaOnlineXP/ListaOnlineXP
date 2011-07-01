#!/bin/sh

javac -encoding utf8 -cp ./ -classpath ./tools.jar Compilar.java
javac -encoding utf8 -cp ./ StreamGobbler.java
javac -encoding utf8 -cp ./ RuntimeExecutor.java
javac -encoding utf8 -cp ./ StringChanger.java
javac -encoding utf8 -cp ./ StringConverter.java
javac -encoding utf8 -cp ./ JavaTester.java
