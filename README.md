## REQUIREMENTS
`python 3.5` or higher because of `**dict` usage

list of required libraries are in `requirements.txt`

## Usage
By running the [`main.py`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/main.py), script will load all `.json` files in `input` folder, convert it to 
specified format and save it to output folder while appending `_SID_format` to the original name. 
I consider `SID` as Specification ID which would be specific to requested data format specification. In that case, we could recognize applied
format just by reading its name.

## Libraries used
I have chosen `pandas` for data manipulation because I am most familiar with this library.
I used `scipy` for Euler to quaternion conversion and `pydantic` for data validation.

## What I have learned

It took me around 12 hours to finish this task. Most of the time was spent on researching
best practices and to understand, for me, new concepts like Euler angles and [Quaternions](
https://www.weizmann.ac.il/sci-tea/benari/sites/sci-tea.benari/files/uploads/softwareAndLearningMaterials/quaternion-tutorial-2-0-1.pdf
). I stumbled upon a [great visualisation](https://eater.net/quaternions) of both quaternions and Euler angles and got introduced to gimbal lock problem.


While I was trying to validate data, I had a feeling that a lot of `if-else` is wrong approach,
so I stumbled upon `pydantic` library for data validation. This is my first time using this library, and I think there is much more to learn tp properly apply this library. 
For my purposes, basic usage as validator was good enough.

While I was doing the conversion I realized the importance of `type-safety` and how it is easy to lose some data properties.
I now understand why I was questioned about `MyPy` on technical interview. I think I should
learn and implement it along the way.


## Improvements
There are many potential improvements, if I had knowledge of best practises.

In the [`config`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/config/config.py) file, I only made one for UAI format, in order to avoid string version of "Magic numbers", where I have previously hardcoded the property names.
The same could be done for Specified format, but I only did it on UAI format to show that I am aware of the problem, but not quite sure
what is the best approach.

I also think there is a better way to convert string values like `"adult"` or `"child"` to `1` or `0`, but I opted for this simple dict approach.
Probably, these values should be used as `Enums` alongside formats in [`config`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/config/config.py) file.

I assume there is a better way to implement the conversion as a part of `pydantic`, but I was not aware of that, therefore
I have chosen my function based approach.

I made several assumptions while writing the code, which you can see as comments having "discussion".
I think these problems are easily solved, for example, the one where, if I don't have UAI specified format within input data, what is my attitude?
There are some bicycles which have value of `"driving"`, even if specification says that these values can only be
`"parked"`, `"stopped"`, `"moving"`. I think in that case no data conversion should be done because we should not give "partial" data to the customer.
But, in order to make this demo complete, in validation phase, I replace `"driving"` with `"moving"` and continue with the execution.

I also think there should be some unit testing on my [`convert_Euler_to_quaternion`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/modules/OrientationCoverter.py)
alongside [`calculate_center_position_from_dimensions`](https://github.com/0meaWaMouShindeiru/UAIconverter/blob/master/modules/PositionConverter.py).

