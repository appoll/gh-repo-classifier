## Fortune Teller

### Setup

First **fork** and *then* clone this repository. Open up the entire folder in Sublime.

`cd` into the folder you just cloned and run the following commands:

    bundle install

    rails server

If it worked, you should be able to navigate to [http://localhost:3000](http://localhost:3000) and see something there. If it didn't work, make sure you don't have any old servers running in other tabs or windows.

### Part 1: Static routes

I've added a list of nav links to [http://localhost:3000/zodiacs/leo](http://localhost:3000/zodiacs/leo), [http://localhost:3000/zodiacs/cancer](http://localhost:3000/zodiacs/cancer), etc.

Currently, none of them work. In `routes.rb`, uncomment each one *one at a time* and make it work. I've planted at least one bug into each RCAV.

**YOUR JOB:** Debug all 12 RCAVs.

### Part 2: DRY it up

Let's do the zodiacs a different way; with a single dynamic route that can handle all 12 signs.

#### Dynamic routes

There's a route at the bottom of `routes.rb` for `/signs/:the_sign`. Uncomment it and make it function. In other words, try going to [http://localhost:3000/signs/whatever](http://localhost:3000/signs/whatever) in Chrome and connect dots until some HTML to shows up. Throw in an `h1` tag with some static content for now.

Next, replace the static content in the `h1` with what the user typed after the slash when they accessed this route. Remember, any parameters (i.e. inputs) coming from the user are accessible in our actions and views in the `params` hash. For example,

    params[:the_sign]

will retrieve what they typed after the slash in this case (assuming that in your route, you named the variable segment of the URL `:the_sign`). Try embedding that in the `h1` tag and capitalizing it.

### Looking up the fortune given the sign

So far so good, but what we really need is the fortune to be dynamically printed in the view along with the name of the sign. To do this, you are going to have to pull the info from somewhere.

I've already prepared the info for you. In this Rails app, you have access to a class called `Zodiac` that I have created (**don't worry about how it works for now - assume it is pulling data from an API or a CSV**).

**Available methods:** 


You can look up single zodiac, given a search criterion, using the `.find_by` method:

    2.1.3 :002 > Zodiac.find_by({ :sign => "leo" })
     =>
    #<Zodiac:0x007fd782f8d548 @creature="lion", @sign="leo", @fortune="Success on all levels is filling your life and making you feel absolutely wonderful, Leo. The downside of this is that you might be a little too conscientious. Are you putting in a lot of extra hours? Be discriminating about this and don't work harder than necessary. You could get stressed to the point of taxing your strength too much, and that won't help you. Pace yourself.">

or

    2.1.3 :002 > Zodiac.find_by({ :creature => "lion" })
     =>
    #<Zodiac:0x007fd782f8d548 @creature="lion", @sign="leo", @fortune="Success on all levels is filling your life and making you feel absolutely wonderful, Leo. The downside of this is that you might be a little too conscientious. Are you putting in a lot of extra hours? Be discriminating about this and don't work harder than necessary. You could get stressed to the point of taxing your strength too much, and that won't help you. Pace yourself.">

As you can see, each `Zodiac` object has three attributes -- creature, sign, and fortune.

Once you have a single `Zodiac` instance, you can access its individual attributes like so:

    2.1.3 :003 > z = Zodiac.find_by({ :sign => "leo" })
    2.1.3 :004 > z.fortune
     =>
    "Success on all levels is filling your life and making you feel absolutely wonderful, Leo. The downside of this is that you might be a little too conscientious. Are you putting in a lot of extra hours? Be discriminating about this and don't work harder than necessary. You could get stressed to the point of taxing your strength too much, and that won't help you. Pace yourself."

You can also do `Zodiac.all` to retrieve an `Array` of all `Zodiac` instances:

    2.1.3 :001 > Zodiac.all
     =>
    [
      #<Zodiac:0x007fd7825d4a60
        @creature="ram",
        @sign="aries",
        @fortune="As your professional dreams unfold, Aries, you may worry about the downside. First, there are new responsibilities that you might doubt your ability to fulfill. Second, you might be catapulted into an uncomfortable new realm of office politics. Don't let these matters put a damper on your enthusiasm. You have what it takes to fulfill the first concern and the wisdom to avoid the second. Onward and upward.">,

      #<Zodiac:0x007fd7825d48f8
        @creature="bull",
        @sign="taurus",
        @fortune="Recent spiritual breakthroughs might have you feeling both exhilarated and downcast, Taurus. Your sensitive side tells you that this is a definite step forward on your spiritual path, but the logical side might cause you to doubt its reality. Take comfort in the fact that reality is relative and that what you're sensing is at least valid for you. Then keep moving ahead.">,

      #<Zodiac:0x007fd782f6e828
        @creature="twins",
        @sign="gemini",
        @fortune="Many of your personal goals have either been met or are in progress, Gemini, and you're feeling exhilarated. However, people around you might have their hands out. You may be asked to contribute to charities or make personal loans to people you don't know well. You want to help whenever you can, but be discriminating about whom you help now. Some may be less than trustworthy.">,

      etc.


**YOUR JOB:** In the `ZodiacsController#sign` action, look up the appropriate zodiac using the user input from the `params` hash. Display the corresponding fortune in the view template.

In other words, these URLs will all work and display both the sign and fortune when you are done:

 - [http://localhost:3000/signs/aries](http://localhost:3000/signs/aries)
 - [http://localhost:3000/signs/taurus](http://localhost:3000/signs/taurus)
 - [http://localhost:3000/signs/gemini](http://localhost:3000/signs/gemini)
 - [http://localhost:3000/signs/cancer](http://localhost:3000/signs/cancer)
 - [http://localhost:3000/signs/leo](http://localhost:3000/signs/leo)
 - [http://localhost:3000/signs/virgo](http://localhost:3000/signs/virgo)
 - [http://localhost:3000/signs/libra](http://localhost:3000/signs/libra)
 - [http://localhost:3000/signs/scorpio](http://localhost:3000/signs/scorpio)
 - [http://localhost:3000/signs/sagittarius](http://localhost:3000/signs/sagittarius)
 - [http://localhost:3000/signs/capricorn](http://localhost:3000/signs/capricorn)
 - [http://localhost:3000/signs/aquarius](http://localhost:3000/signs/aquarius)
 - [http://localhost:3000/signs/pisces](http://localhost:3000/signs/pisces)

**YOUR OTHER JOB:** Similarly, make all these URLs work:

 - [http://localhost:3000/creatures/ram](http://localhost:3000/creatures/ram)
 - [http://localhost:3000/creatures/bull](http://localhost:3000/creatures/bull)
 - [http://localhost:3000/creatures/twins](http://localhost:3000/creatures/twins)
 - [http://localhost:3000/creatures/crab](http://localhost:3000/creatures/crab)
 - [http://localhost:3000/creatures/lion](http://localhost:3000/creatures/lion)
 - [http://localhost:3000/creatures/maiden](http://localhost:3000/creatures/maiden)
 - [http://localhost:3000/creatures/scales](http://localhost:3000/creatures/scales)
 - [http://localhost:3000/creatures/scorpion](http://localhost:3000/creatures/scorpion)
 - [http://localhost:3000/creatures/archer](http://localhost:3000/creatures/archer)
 - [http://localhost:3000/creatures/goat](http://localhost:3000/creatures/goat)
 - [http://localhost:3000/creatures/waterbearer](http://localhost:3000/creatures/waterbearer)
 - [http://localhost:3000/creatures/fish](http://localhost:3000/creatures/fish)

using a second flexible, smart RCAV.

Your goal is to make your app work like [this target](https://fortune-teller-target.herokuapp.com).

