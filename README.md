# Welcome to Mars File source code repository!
## What is this?
Mars File is another configuration file, for now only supported by my Python module, which itself is open-source!
If you wish, you can create libraries/modules for other programming languages!
But remember, MF isn't created to compete with other configuration languages, like XML, JSON, INI, YAML, etc; it's made purely to be easy to use, and straight-forward! 💟

## Syntax (1.2)
Warning, upcoming version 1.3 will change IDs of entries dramatically! Please be sure to look for changes!
```
$<1.2>
` I'm some random comment!
[s~headerName]
{s~stringType/I'm just a string value!}
{c~comboType/we;are;just;combo;values;}
{n~numberType/1234567890}
[e~headerName]
`
[s~marsFile]
{s~example/Hello World!}
[e~marsFile]
```
Okay-okay, for starters:
- Version tags (`$<1.1>`) are a must on 1.1 and up
- No empty lines, instead, use empty comments!
- Every header (`[s~headerName]`) needs it's own ender (`[e~headerName]`)! *Don't make them alone :crying_cat_face:*
- Never use `{}` without indicators (`s`, `c`, `n`)! :heart:

This done.. now some more explanations!

#### Version Tags:
`$<...>`
- As mentioned before, from syntax 1.1 and up they are a must, to put it simple, this is needed for the parser to check if your locally installed build is compatible with the MFC syntax version specified in that file.

#### Headers:
`[...~...]`
- First goes `s` for *starter*, or `e` for *ender*. Then goes section value, which can be anything, but **no** spaces.

#### Entries:
`{...~.../...}`
- First goes indicator `s` for *string*, `c` for *combo* and `n` for *number*. Then goes the entry name, which can be anything, but **no** spaces. Then goes your actual value, spaces allowed! :smile_cat:

#### Comments:
- Anything after the \` will be ignored, **BUT** putting it after a *(for example)* header or entry **will** result in a syntax! :crying_cat_face:
Example of invalid use:
```
$<1.1>
[s~marsFile] `im an illegal comment
{s~example/Hello World!}`im an illegal comment too!
[e~marsFile]
` haha, im legal!!!!!
```

## To-do
*Will be updated later...*
