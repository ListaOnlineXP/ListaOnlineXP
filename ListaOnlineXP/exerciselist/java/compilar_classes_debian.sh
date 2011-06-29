#!/bin/sh

javac -encoding utf8 -cp ./ -classpath /usr/lib/jvm/java-6-sun/lib/tools.jar Compilar.java;
javac -encoding utf8 -cp ./ StreamGobbler.java
javac -encoding utf8 -cp ./ RuntimeExecutor.java
javac -encoding utf8 -cp ./ StringChanger.java
javac -encoding utf8 -cp ./ StringConverter.java
javac -encoding utf8 -cp ./ JavaTester.java
