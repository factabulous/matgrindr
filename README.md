Introduction
====

Matgrindr is a plugin for EDMC that allows you to specify which 
materials you are looking for in Elite Dangerous. It will then 
direct you to locations for those materials and tell you what 
to do when you get there.

It does this by using lists of locations derived from Canonn datasets.

At the moment it can guide you to:
* Thargoid Sensors (at crash sites), 
* Thargoid Links (at Thargoid Structures) 
* Raw materials at Brain Tree sites.

Note that the data in not ideal at the moemnt - it includes Thargoid Structures
that are inactive, and Brain Tree sites that have been invalidated (though
there are few of these). The list is updated daily, it is downloaded from 
a google doc daily so will improve over time. 

Prerequistes
----

You will need EDMC installed https://github.com/Marginal/EDMarketConnector/wiki

Installation
----

Unzip the plugin into EDMCs plugins directory. It appears as a plugin called
matgrindr-release - there is a settings page to set what you need, and the 
status should show on the main EDMC page. 

Usage
----

In the settings page select the items you want. 

If there is nothing that matches in the current system then you will be 
prompted with the nearest location. There is an icon to copy the system
name to your clipboard.

Once you are in the correct system you will be told which planet to 
travel to. You must choose the correct planet.

If you need to find a location on a planet it will tell you the a target 
heading to get there once you enter planetary cruise - it is
recommended to set EDMC to 'always on top' so you can see the heading.

The angle of descent is only shown once it is at least 30 degrees - it's recommended to start descent a bit later as if your angle becomes less than 30 degree
you will not be able to see it.

On landing you will be told what you can harvest from your list. Brain Trees
require shooting the materials from trees.

When you take off again you will be told a new target. In the case of Brain
Trees they can only be harvested every week, so a visited site will not be
suggested again once visited within the week. Thargoid Sensors (and Links) 
however can be revisited / reharvested immediatley, so these will immediately
direct you back to the planet, it is suggested that you de-select these items
after you have harvested them.

Third Parties
-----

Icons provided by Iconic https://useiconic.com/open

