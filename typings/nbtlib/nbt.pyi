"""
This type stub file was generated by pyright.
"""

from .tag import Compound

"""
.. testsetup::

    import io
    import nbtlib
    from nbtlib import *

The library supports reading and writing nbt data in all its forms and
treats everything as uncompressed big-endian nbt by default.

You can load nbt files with the :func:`load` function.

.. doctest::

    >>> nbtlib.load("docs/hello_world.nbt")
    <File 'hello world': Compound({...})>

The function will figure out by itself if the file is gzipped before loading
it. You can set the ``byteorder`` parameter to ``"little"`` if the file is
little-endian.

.. doctest::

    >>> nbtlib.load("docs/hello_world_little.nbt", byteorder="little")
    <File 'hello world': Compound({...})>

You can create new nbt files by instantiating the :class:`File` class with
the desired nbt data and calling the :meth:`File.save` method.


.. doctest::

    >>> nbt_file = nbtlib.File({"demo": Compound({"counter": Int(0)})})
    >>> nbt_file.save("docs/demo.nbt")
    >>> nbtlib.load("docs/demo.nbt")
    <File 'demo': Compound({'counter': Int(0)})>

The :meth:`File.save` method can output gzipped or little-endian nbt
by using the ``gzipped`` and ``byteorder`` arguments respectively.

.. doctest::

    >>> demo = nbtlib.load("docs/demo.nbt")

    >>> # overwrite
    >>> demo.save()

    >>> # make a gzipped copy
    >>> demo.save("docs/demo_copy.nbt", gzipped=True)

    >>> # convert the file to little-endian
    >>> demo.save("docs/demo_little.nbt", byteorder="little")
"""
__all__ = ["load", "File"]
def load(filename, *, gzipped=..., byteorder=...): # -> File:
    """Load the nbt file at the specified location.

    .. doctest::

        >>> nbt_file = nbtlib.load("docs/bigtest.nbt")
        >>> nbt_file["stringTest"]
        String('HELLO WORLD THIS IS A TEST STRING ÅÄÖ!')

    The function returns an instance of the dict-like :class:`File` class
    holding all the data that could be parsed from the binary file.
    You can retrieve items with the index operator just like with regular python
    dictionaries.

    Note that the :class:`File` instance can be used as a context
    manager. The :meth:`File.save` method is called automatically at the
    end of the ``with`` statement.

    .. doctest::

        >>> with nbtlib.load("docs/demo.nbt") as demo:
        ...     demo["counter"] = nbtlib.Int(demo["counter"] + 1)


    Arguments:
        gzipped: Whether the file is gzipped or not.

            If the argument is not specified, the function will read the
            magic number of the file to figure out if the file is
            gzipped.

            .. doctest::

                >>> filename = "docs/hello_world.nbt"
                >>> nbt_file = nbtlib.load(filename, gzipped=False)
                >>> nbt_file.gzipped
                False

            The function simply delegates to :meth:`File.load`
            when the argument is specified explicitly.

        byteorder: Whether the file is big-endian or little-endian.

            The default value is ``"big"`` so files are interpreted as
            big-endian if the argument is not specified. You can set the
            argument to ``"little"`` to handle little-endian nbt data.

            .. doctest::

                >>> filename = "docs/hello_world_little.nbt"
                >>> nbt_file = nbtlib.load(filename, byteorder="little")
                >>> nbt_file.byteorder
                'little'
    """
    ...

class File(Compound):
    r"""Class representing a compound nbt file.

    .. doctest::

        >>> nbt_file = nbtlib.File({
        ...     "Data": nbtlib.Compound({
        ...         "hello": nbtlib.String("world")
        ...    })
        ... })

    The class inherits from :class:`Compound`, so all the builtin ``dict``
    operations inherited by the :class:`nbtlib.tag.Compound` class are
    also available on :class:`File` instances.

    .. doctest::

        >>> nbt_file.items()
        dict_items([('Data', Compound({'hello': String('world')}))])
        >>> nbt_file["Data"]
        Compound({'hello': String('world')})

    You can write nbt data to an already opened file-like object with the
    inherited :meth:`nbtlib.tag.Compound.write` method.

    .. doctest::

        >>> fileobj = io.BytesIO()
        >>> nbt_file.write(fileobj)
        >>> fileobj.getvalue()
        b'\n\x00\x04Data\x08\x00\x05hello\x00\x05world\x00'

    If you need to load files from an already opened file-like object, you can
    use the inherited :meth:`nbtlib.tag.Compound.parse` classmethod.

    .. doctest::

        >>> fileobj.seek(0)
        0
        >>> nbtlib.File.parse(fileobj) == nbt_file
        True

    Attributes:
        filename:
            The name of the file, ``None`` by default. The attribute is
            set automatically when the file is returned from the
            :func:`load` helper function and can also be set in the
            constructor.

            .. doctest::

                >>> nbt_file.filename is None
                True
                >>> nbtlib.load("docs/demo.nbt").filename
                'docs/demo.nbt'

        gzipped:
            Boolean indicating if the file is gzipped. The attribute can
            also be set in the constructor. New files are uncompressed
            by default.

            .. doctest::

                >>> nbtlib.File(nbt_file, gzipped=True).gzipped
                True

        byteorder:
            The byte order, either ``"big"`` or ``"little"``. The
            attribute can also be set in the constructor. New files are
            big-endian by default.

            .. doctest::

                >>> nbtlib.File(nbt_file, byteorder="little").byteorder
                'little'
    """
    def __init__(self, *args, gzipped=..., byteorder=..., filename=..., root_name=...) -> None:
        ...
    
    @classmethod
    def parse(cls, fileobj, byteorder=...): # -> Self:
        """Override :meth:`nbtlib.tag.Base.parse` for nbt files."""
        ...
    
    def write(self, fileobj, byteorder=...): # -> None:
        """Override :meth:`nbtlib.tag.Base.write` for nbt files."""
        ...
    
    @classmethod
    def from_fileobj(cls, fileobj, byteorder=...): # -> Self:
        """Load an nbt file from a proper file object.

        The method is used by the :func:`load` helper function when the
        ``gzipped`` keyword-only argument is not specified explicitly.

        Arguments:
            fileobj:
                Can be either a standard ``io.BufferedReader`` for
                uncompressed nbt or a ``gzip.GzipFile`` for gzipped nbt
                data. The function simply calls the inherited
                :meth:`nbtlib.tag.Compound.parse` classmethod and sets the
                :attr:`filename` and :attr:`gzipped` attributes depending
                on the argument.

            byteorder:
                Can be either ``"big"`` or ``"little"``. The argument is
                forwarded to :meth:`nbtlib.tag.Compound.parse`.
        """
        ...
    
    @classmethod
    def load(cls, filename, gzipped, byteorder=...): # -> Self:
        """Read, parse and return the nbt file at the specified location.

        The method is used by the :func:`load` helper function when the
        ``gzipped`` keyword-only argument is specified explicitly.
        The function opens the file and uses :meth:`from_fileobj` to return
        the :class:`File` instance.

        Arguments:
            filename: The name of the file.
            gzipped: Whether the file is gzipped or not.
            byteorder: Can be either ``"big"`` or ``"little"``.
        """
        ...
    
    def save(self, filename=..., *, gzipped=..., byteorder=...): # -> None:
        """Write the file at the specified location.

        The method is called without any argument at the end of ``with``
        statements when the :class:`File` instance is used as a
        context manager.

        .. doctest::

            >>> with demo:
            ...     demo['counter'] = nbtlib.Int(0)

        This essentially overwrites the file at the end of the ``with`` statement.

        Arguments:
            filename: The name of the file. Defaults to the instance's :attr:`filename` attribute.
            gzipped: Whether the file should be gzipped. Defaults to the instance's :attr:`gzipped` attribute.
            byteorder: Whether the file should be big-endian or little-endian. Defaults to the instance's :attr:`byteorder` attribute.
        """
        ...
    
    def __enter__(self): # -> Self:
        ...
    
    def __exit__(self, exc_type, exc_val, exc_tb): # -> None:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __repr__(self): # -> str:
        ...
    


