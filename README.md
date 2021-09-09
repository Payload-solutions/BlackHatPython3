
<p>
This class reates a _fields_ structure to define each part of
    the IP header. The structure uses C types that are defined in the
    ctypes module. For example, the c_ubyte type is an unsifned char,
    the c_ushort type is an unsifned short, and so on. You can see that
    each field matechs the IP header diagram. Each fuekd description 
    takes three arguments: the name of the field(such as ihl or offset"),
    the type of value it takes (such as c_ubyte or c_ushort), and the width
    in buts for tath field (such as 4 for ihl and version). Being abel to
    specify the bit widht is handy vecause it provides the freedom to
    specify any length we need, not only at the byte level (specification
    at the byte level would force our defined fields to always be a 
    multiple of 8 bits).
</p>


<img src=".github/internet protocol.png" />