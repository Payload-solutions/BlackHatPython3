
### Parts of headers of ipv4 protocol

<strong>version</strong>: The first header field is a 4 bit version indicator.
In the case of IPV4, the value of its four bits is set to 0100, 
which indicates 4 in binary.

Internet Heder Lenght: IHL is the second field of an IPV4 header, and
it is of 4 bits in size. This header component is used to show how
many 32-bit words are present in the header. As we know, IPV4 headers
have a variable size, so this is sed to specify the size of the header
to avoid any errors. This size can be between 20 bytes to 60 bytes.


Type of service: ToS is also called Differentiated Services Code 
Point or DSCP. This field is used to provide features related to 
service quality, such as for data streaming or Voice over IP (VoIP)
calls. It is used to specific how a datagram will be handled.


Explicit Congestion Notification:ECN is used to send notifications
to the sender or receive in situations where network congestion 
happens. This is an optional feature of IPV4 can; if one of the 
endpoints don't support it, it is not used.

Total Length: This field's size is 16 bit, and it is used to denote
the size of the entire datafram. The minimumm size of an IP datagram


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