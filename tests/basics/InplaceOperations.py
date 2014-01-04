#     Copyright 2014, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Python tests originally created or extracted from other peoples work. The
#     parts were too small to be protected.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
x = 1
x += 2

print "Plain inplace:", x

z = [ 1, 2, 3 ]
z[1] += 5

print "List inplace:", z[1]

h = { "a" : 3 }
h["a"] += 2

print "Dict inplace:", h["a"]

class B:
    a = 1

B.a += 2

print "Class attribute inplace:", B.a

h = [ 1, 2, 3, 4 ]
h[1:2] += (2,3)

print "List sclice inplace [x:y]", h

h[:1] += (9,9)

print "List sclice inplace [:y]", h

h[2:] += (6,6)

print "List sclice inplace [y:]", h

h[:] += (5,5,5)

print "List sclice inplace [:]", h
