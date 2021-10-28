"""
A simple data class to collect AaC command info from plugins.
"""
import attr


@attr.s
class AacCommandArgument:
    """
    A class used as a struct to hold a command argument name and description.

    Attributes:
        name: A string with the name of the command argument
        description: a string with the command argument description -- will provide a description
                        about this argument when the help command is invoked.
        number_of_arguments: Number of entries that the argument can take. Maps to the argsparse module's nargs command.
    """

    name = attr.ib(validator=attr.validators.instance_of(str))
    description = attr.ib(validator=attr.validators.instance_of(str))
    number_of_arguments = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))


@attr.s
class AacCommand:
    """
    A class used as a struct to hold a command name, command description, and callback.
    The command name is added to the argument parser with help set to teh command description.
    The callback is invoked if the user specifies the command.

    Attributes:
        command_name: A string with the name of the command_description
        command_description: a string with the command description -- will be provided with the help command
        callback: A Callable function that's executed when the user runs the AaC command
        arguments: A List of AacCommandArgument containing argument information about the command. Defaults to an empty list.
    """

    name = attr.ib(validator=attr.validators.instance_of(str))
    description = attr.ib(validator=attr.validators.instance_of(str))
    callback = attr.ib(validator=attr.validators.is_callable())
    arguments = attr.ib(default=[], validator=attr.validators.instance_of(list))
