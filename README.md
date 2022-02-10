## REQUIREMENTS
`python 3.5` or higher because of `**dict` usage

list of required libraries are in `requirements.txt`

## Usage
By running the [`main.py`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/main.py), script will load all `.json` files in `input` folder, convert it to 
specified format and save it to output folder with appending `_SID_format` to the original name. 
I consider `SID` as Specification ID and something that would be specific to this data format specification so that we know which
format was applied to this data just by reading it's name.

## Libraries used
I have chosen `pandas` for data manipulation because I am most familiar with this library.
I used `scipy` for Euler to quaternion conversion and `pydantic` for data validation.

## What I have learned

It took me around 12 hours to finish this task. Most of the time was spent on researching
best practices and to understand, for me, new concepts like euler angles and [Quaternions](
https://www.weizmann.ac.il/sci-tea/benari/sites/sci-tea.benari/files/uploads/softwareAndLearningMaterials/quaternion-tutorial-2-0-1.pdf
). I stumbled upon a [great visualisation](https://eater.net/quaternions) of both quaternions and Euler angles and got introduced to gimbal lock problem.


While I was trying to validate data, I had a feeling that a lot of `if-else` is wrong approach,
so I stumbled upon `pydantic` library for data validation. This is my first time that I am using this library, and I think there is much more to learn in applying this library. For my validation purposes, basic usage was good enough.

While I was doing the conversion I realized the importance of `type-safety` and how it is easy to lose some data properties.
I think that now I understand why I was question about `MyPy` on technical interview and it is something that I think I should
learn along the way.


## Improvements
There are a lot of things that could be improved if I had knowledge of what is the best practise.

In the [`config`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/config/config.py) file, I only made one for UAI format, in order to avoid string version of "Magic numbers", where I hardcoded the property names.
The same could be done for Specified format, but I only did it on UAI format to show that I am aware of the problem, but not quite sure
what is the best approach.

I also think there is a better way to convert string values like `"adult"` or `"child"` to `1` or `0`, but I opted for this simple dict approach.
Probably, these values should be used as `Enums` alongside formats in [`config`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/config/config.py) file.

I think that there is a better way to do the conversion as a part of `pydantic`, but I was not aware of that, therefore
I have chosen my function based approach.

I made several assumptions while writing the code, which you can see in code with "discussion" in its comment.
I think these problems are easily solved, for example, the one if I don't have UAI specified format within input data, what is my attitude?
There are some bicycles which have value of `"driving"`, even if specification says that these values can only be
`"parked"`, `"stopped"`, `"moving"`. I think in that case no data conversion should be done because we should not give "partial" data to the customer.
But, in order to make this demo complete, in validation phase, I replace `"driving"` with `"moving"` and continue with the execution.

I also think there should be some kind of unit testing on my [`convert_Euler_to_quaternion`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/modules/OrientationCoverter.py)
alongside [`calculate_center_position_from_dimensions`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/modules/PositionConverter.py).

