= Spring Boot image:https://build.spring.io/plugins/servlet/buildStatusImage/BOOT-PUB["Build Status", link="https://build.spring.io/browse/BOOT-PUB"] image:https://badges.gitter.im/Join Chat.svg["Chat",link="https://gitter.im/spring-projects/spring-boot?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge"]
:docs: http://docs.spring.io/spring-boot/docs/current-SNAPSHOT/reference

Spring Boot makes it easy to create Spring-powered, production-grade applications and
services with absolute minimum fuss. It takes an opinionated view of the Spring platform
so that new and existing users can quickly get to the bits they need.

You can use Spring Boot to create stand-alone Java applications that can be started using
`java -jar` or more traditional WAR deployments. We also provide a command line tool
that runs spring scripts.

Our primary goals are:

* Provide a radically faster and widely accessible getting started experience for all
Spring development
* Be opinionated out of the box, but get out of the way quickly as requirements start to
diverge from the defaults
* Provide a range of non-functional features that are common to large classes of projects
(e.g. embedded servers, security, metrics, health checks, externalized configuration)
* Absolutely no code generation and no requirement for XML configuration



== Installation and Getting Started
The {docs}/htmlsingle/[reference documentation] includes detailed
{docs}/htmlsingle/#getting-started-installing-spring-boot[installation instructions]
as well as a comprehensive {docs}/htmlsingle/#getting-started-first-application[``getting
started``] guide. Documentation is published in {docs}/htmlsingle/[HTML],
{docs}/pdf/spring-boot-reference.pdf[PDF] and {docs}/epub/spring-boot-reference.epub[EPUB]
formats.

Here is a quick teaser of a complete Spring Boot application in Java:

[source,java,indent=0]
----
	import org.springframework.boot.*;
	import org.springframework.boot.autoconfigure.*;
	import org.springframework.web.bind.annotation.*;

	@RestController
	@SpringBootApplication
	public class Example {

		@RequestMapping("/")
		String home() {
			return "Hello World!";
		}

		public static void main(String[] args) throws Exception {
			SpringApplication.run(Example.class, args);
		}

	}
----



== Getting help
Having trouble with Spring Boot? We'd like to help!

* Check the {docs}/htmlsingle/[reference documentation], especially the
  {docs}/htmlsingle/#howto[How-to's] -- they provide solutions to the most common
  questions.
* Learn the Spring basics -- Spring Boot builds on many other Spring projects, check
  the http://spring.io[spring.io] web-site for a wealth of reference documentation. If
  you are just starting out with Spring, try one of the http://spring.io/guides[guides].
* Ask a question - we monitor http://stackoverflow.com[stackoverflow.com] for questions
  tagged with http://stackoverflow.com/tags/spring-boot[`spring-boot`].
* Report bugs with Spring Boot at https://github.com/spring-projects/spring-boot/issues[github.com/spring-projects/spring-boot/issues].



== Reporting Issues
Spring Boot uses GitHub's integrated issue tracking system to record bugs and feature
requests. If you want to raise an issue, please follow the recommendations below:

* Before you log a bug, please https://github.com/spring-projects/spring-boot/search?type=Issues[search the issue tracker]
  to see if someone has already reported the problem.
* If the issue doesn't already exist, https://github.com/spring-projects/spring-boot/issues/new[create a new issue].
* Please provide as much information as possible with the issue report, we like to know
  the version of Spring Boot that you are using, as well as your Operating System and
  JVM version.
* If you need to paste code, or include a stack trace use Markdown +++```+++ escapes
  before and after your text.
* If possible try to create a test-case or project that replicates the issue. You can
  submit sample projects as pull-requests against the
  https://github.com/spring-projects/spring-boot-issues[spring-boot-issues] GitHub
  project. Use the issue number for the name of your project.



== Building from Source
You don't need to build from source to use Spring Boot (binaries in
http://repo.spring.io[repo.spring.io]), but if you want to try out the latest and
greatest, Spring Boot can be easily built with the
https://github.com/takari/maven-wrapper[maven wrapper]. You also need JDK 1.8 (although
Boot applications can run on Java 1.6).

[indent=0]
----
	$ ./mvnw clean install
----

If you want to build with the regular `mvn` command, you will need
http://maven.apache.org/run-maven/index.html[Maven v3.2.1 or above].

NOTE: You may need to increase the amount of memory available to Maven by setting
a `MAVEN_OPTS` environment variable with the value `-Xmx512m`. Remember
to set the corresponding property in your IDE as well if you are building and running
tests there (e.g. in Eclipse go to `Preferences->Java->Installed JREs` and edit the
JRE definition so that all processes are launched with those arguments). This property
is automatically set if you use the maven wrapper.

_Also see link:CONTRIBUTING.adoc[CONTRIBUTING.adoc] if you wish to submit pull requests,
and in particular please fill out the
https://support.springsource.com/spring_committer_signup[Contributor's Agreement]
before your first change, however trivial. (Or if you filed such an agreement already for
another project just mention that in your pull request.)_

=== Building reference documentation

The reference documentation requires the documentation of the Maven plugin to be
available so you need to build that first since it's not generated by default.

[indent=0]
----
	$ ./mvnw clean install -pl spring-boot-tools/spring-boot-maven-plugin -Pdefault,full
----

The documentation also includes auto-generated information about the starters. To
allow this information to be collected, the starter projects must be built first:

[indent=0]
----
	$ ./mvnw clean install -f spring-boot-starters
----

Once this is done, you can build the reference documentation with the command below:

[indent=0]
----
	$ ./mvnw clean prepare-package -pl spring-boot-docs -Pdefault,full
----

TIP: The generated documentation is available from `spring-boot-docs/target/contents/reference`


== Modules
There are a number of modules in Spring Boot, here is a quick overview:



=== spring-boot
The main library providing features that support the other parts of Spring Boot,
these include:

* The `SpringApplication` class, providing static convenience methods that make it easy
to write a stand-alone Spring Application. Its sole job is to create and refresh an
appropriate Spring `ApplicationContext`
* Embedded web applications with a choice of container (Tomcat or Jetty for now)
* First class externalized configuration support
* Convenience `ApplicationContext` initializers, including support for sensible logging
defaults



=== spring-boot-autoconfigure
Spring Boot can configure large parts of common applications based on the content
of their classpath. A single `@EnableAutoConfiguration` annotation triggers
auto-configuration of the Spring context.

Auto-configuration attempts to deduce which beans a user might need. For example, If
`HSQLDB` is on the classpath, and the user has not configured any database connections,
then they probably want an in-memory database to be defined. Auto-configuration will
always back away as the user starts to define their own beans.



=== spring-boot-starters
Starters are a set of convenient dependency descriptors that you can include in
your application. You get a one-stop-shop for all the Spring and related technology
that you need without having to hunt through sample code and copy paste loads of
dependency descriptors. For example, if you want to get started using Spring and JPA for
database access just include the `spring-boot-starter-data-jpa` dependency in your
project, and you are good to go.



=== spring-boot-cli
The Spring command line application compiles and runs Groovy source, making it super
easy to write the absolute minimum of code to get an application running. Spring CLI
can also watch files, automatically recompiling and restarting when they change.



=== spring-boot-actuator
Spring Boot Actuator provides additional auto-configuration to decorate your application
with features that make it instantly deployable and supportable in production.  For
instance if you are writing a JSON web service then it will provide a server, security,
logging, externalized configuration, management endpoints, an audit abstraction, and
more. If you want to switch off the built in features, or extend or replace them, it
makes that really easy as well.



=== spring-boot-loader
Spring Boot Loader provides the secret sauce that allows you to build a single jar file
that can be launched using `java -jar`. Generally you will not need to use
`spring-boot-loader` directly, but instead work with the
link:spring-boot-tools/spring-boot-gradle-plugin[Gradle] or
link:spring-boot-tools/spring-boot-maven-plugin[Maven] plugin.



== Samples
Groovy samples for use with the command line application are available in
link:spring-boot-cli/samples[spring-boot-cli/samples]. To run the CLI samples type
`spring run <sample>.groovy` from samples directory.

Java samples are available in link:spring-boot-samples[spring-boot-samples] and should
be built with maven and run by invoking `java -jar target/<sample>.jar`.



== Guides
The http://spring.io/[spring.io] site contains several guides that show how to use Spring
Boot step-by-step:

* http://spring.io/guides/gs/spring-boot/[Building an Application with Spring Boot] is a
  very basic guide that shows you how to create a simple application, run it and add some
  management services.
* http://spring.io/guides/gs/actuator-service/[Building a RESTful Web Service with Spring
  Boot Actuator] is a guide to creating a REST web service and also shows how the server
  can be configured.
* http://spring.io/guides/gs/convert-jar-to-war/[Converting a Spring Boot JAR Application
  to a WAR] shows you how to run applications in a web server as a WAR file.



== License
Spring Boot is Open Source software released under the
http://www.apache.org/licenses/LICENSE-2.0.html[Apache 2.0 license].
