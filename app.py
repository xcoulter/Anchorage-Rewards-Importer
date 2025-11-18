import streamlit as st
import pandas as pd
import io
from datetime import datetime
from calendar import monthrange
import uuid
import re

# Set page title
st.title("Transaction CSV Converter")

# Embedded Wallets List CSV content
wallets_csv = """name,id,description,type,deviceType,networkId,address,addresses,path,enabledCoins,__typename
Aptos - Do Kwon,OA22N5lsoDwyPQoOE7xE,,9,,apt,,0x5aba5dd7021e53e8ee3aab8e0759ff3a634cb52c83c149dbea812c064f5c1b4b,,,Wallet
Aptos Mainnet Wallet 1,andkqueGsZgGJKiJWP5T,,9,,apt,,0xca78412b2d681145a88a771b4f7d5ea36bb949b7352d9415c4c1f46a7ac7acf7,,,Wallet
Aptos Mainnet Wallet 1 vesting tokens,apt.0x.0xca78412b2d681145a88a771b4f7d5ea36bb949b7352d9415c4c1f46a7ac7acf7,,22,,,,,,,Wallet
Aptos Mainnet Wallet 10,suQDAlfgAQafSGqrSVzM,,9,,apt,,0x03150576115e2c791261359f0d71dec72799f7ed87620f609420d6e03265e7e7,,,Wallet
Aptos Mainnet Wallet 10 vesting tokens,apt.0x.0x03150576115e2c791261359f0d71dec72799f7ed87620f609420d6e03265e7e7,,22,,,,,,,Wallet
Aptos Mainnet Wallet 100,CmFK9X9GYYKcdK1VR9vW,,9,,apt,,0x2db22014a577bca5d9e17fefbad3d14c94249f6be5069a6910706d88071a458c,,,Wallet
Aptos Mainnet Wallet 100 Staked Balance,apt.0x.0x2db22014a577bca5d9e17fefbad3d14c94249f6be5069a6910706d88071a458c,,22,,,,,,,Wallet
Aptos Mainnet Wallet 102,jDwokH35UobCgSkx0rbh,,9,,apt,,0x49b1cf68f684f08393c813f42623626a0cbb45bb65aa3e34fdf89519573575ee,,,Wallet
Aptos Mainnet Wallet 102 vesting tokens,apt.0x.0x49b1cf68f684f08393c813f42623626a0cbb45bb65aa3e34fdf89519573575ee,,22,,,,,,,Wallet
Aptos Mainnet Wallet 103,kp5SnhBLzUq3KlYa0NfA,,9,,apt,,0x6151a52845b113c7db63c9d5b7d0c73e12db1018bb85ae625c382b521f508f76,,,Wallet
Aptos Mainnet Wallet 103 vesting tokens,apt.0x.0x6151a52845b113c7db63c9d5b7d0c73e12db1018bb85ae625c382b521f508f76,,22,,,,,,,Wallet
Aptos Mainnet Wallet 104,RPB5Nu6gJMR167KoLXg8,,9,,apt,,0x14feff5a873d3c6ce8694ce984eb179318fca2b4ac7b39bda2417be45eb6f7d8,,,Wallet
Aptos Mainnet Wallet 104 vesting tokens,apt.0x.0x14feff5a873d3c6ce8694ce984eb179318fca2b4ac7b39bda2417be45eb6f7d8,,22,,,,,,,Wallet
Aptos Mainnet Wallet 105,PAqxUKTcV8qLUwU1mF3i,,9,,apt,,0xced7fd303286dd08181a4519b472350ea4c79468acf50a8eb657dd249ddf9bbc,,,Wallet
Aptos Mainnet Wallet 105 vesting tokens,apt.0x.0xced7fd303286dd08181a4519b472350ea4c79468acf50a8eb657dd249ddf9bbc,,22,,,,,,,Wallet
Aptos Mainnet Wallet 106,f3F0bCUVpVxnQXJ9bc2Y,,9,,apt,,0xfe538f0ea4514e360e636ee62df8d19cb9ed46c31296b7920c69e8b67685fa0d,,,Wallet
Aptos Mainnet Wallet 106 vesting wallets,apt.0x.0xfe538f0ea4514e360e636ee62df8d19cb9ed46c31296b7920c69e8b67685fa0d.0x,,22,,,,,,,Wallet
Aptos Mainnet Wallet 108,imacMwU1ZKdH8y7JGQE3,,9,,apt,,0xfeba00184ee586791e741485ca7579e32168fcd78224f65d7add9defe9abbe52,,,Wallet
Aptos Mainnet Wallet 108 vesting tokens,apt.0xc4599c79e78aa795b14633f035ae9755dee9600927624d11a8064acc6f305486.0xc4599c79e78aa795b14633f035ae9755dee9600927624d11a8064acc6f305486.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 109,Rbivs54KbiftgY86yiw1,,9,,apt,,0x53f6882b38de7d94dad91359d28647a5245985eda0d3953e3c23aaaa2dc2016e,,,Wallet
Aptos Mainnet Wallet 109 vesting tokens,apt.0x.0x53f6882b38de7d94dad91359d28647a5245985eda0d3953e3c23aaaa2dc2016e,,22,,,,,,,Wallet
Aptos Mainnet Wallet 110,nIzAZ6DcNvI7VGu684zt,,9,,apt,,0x7664cec5d893f8ca41d69621a31920a9310488405936e346749035feb2abad81,,,Wallet
Aptos Mainnet Wallet 110 vesting tokens,apt.0x1.0x9189f547224e8136338649c3bc3ea3af5ae81e165c83fb3afcd356b0b00ad4be.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 113,pXKIhJyuuyE0Z0t76UrQ,,9,,apt,,0xa162e0449405eeae3b492eb9cd24534d32e0bdb1cc92c1083cfbd6d712efb89b,,,Wallet
Aptos Mainnet Wallet 113 vesting tokens,apt.0x1.0x4a37786aa960a0fa8b5d547182b61d41be313aedc6c8a6a62b2ebc8a9496db5a.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 114,Bq2e52546c5wjIl1B76b,,9,,apt,,0xe3dab0aa348eee08c8e0cc9ecf56650ad9f9a98b78224ca045abd50bea3503dd,,,Wallet
Aptos Mainnet Wallet 114 Staked Balance,apt.0x.0xe3dab0aa348eee08c8e0cc9ecf56650ad9f9a98b78224ca045abd50bea3503dd,,22,,,,,,,Wallet
Aptos Mainnet Wallet 115,izT2HH8HFRYysabO2vI2,,9,,apt,,0xf8174d6de06b5ff961279015d5c080902ff19f20bcb2d1bc109d9efa4eeee2e8,,,Wallet
Aptos Mainnet Wallet 118,4nzac2QDRAnTXgHDG4zn,,9,,apt,,0xac426d1b7372f4bfee01c1908ab50ababe8fd5330f593d56926d25d38e53e21b,,,Wallet
Aptos Mainnet Wallet 118 vesting tokens,apt.0x.0xac426d1b7372f4bfee01c1908ab50ababe8fd5330f593d56926d25d38e53e21b,,22,,,,,,,Wallet
Aptos Mainnet Wallet 119,dXnkhsINhrRBJNARcCBN,,9,,apt,,0xe266a1b119c6c149a76a66cfd017514bdd8f9191cf53a8d3c40baaca405f16de,,,Wallet
Aptos Mainnet Wallet 126,jfG5i7Q9gOoUwEaYhVtt,,9,,apt,,0xc466f174b6533c1516b9389ec50e7d518369f08cbef8815a7308a6462ed5fb0b,,,Wallet
Aptos Mainnet Wallet 127,vhYBmsgDWKRAjnqWZYAg,,9,,apt,,0x07f8a3e094c96db6e44442e1c35a1fd0314694db111895ac3adc462f891e8504,,,Wallet
Aptos Mainnet Wallet 127 vesting tokens,apt.0x.0x07f8a3e094c96db6e44442e1c35a1fd0314694db111895ac3adc462f891e8504,,22,,,,,,,Wallet
Aptos Mainnet Wallet 128,oIkaD1vdQjuIw6j4yYRO,,9,,apt,,0xecc2110cd190b2101709b5d51674379ee8005cffa29f2d3344c083cbff25b13d,,,Wallet
Aptos Mainnet Wallet 130,aTT9KGt9djnwZxKwEoDq,,9,,apt,,0xfcc0da16fd27ff72a0d3d82b9b2b2a6a238814f3f0440362b2462ab3d2dd975b,,,Wallet
Aptos Mainnet Wallet 130 vesting tokens,apt.0x.0xfcc0da16fd27ff72a0d3d82b9b2b2a6a238814f3f0440362b2462ab3d2dd975b,,22,,,,,,,Wallet
Aptos Mainnet Wallet 132,tAHJwuE9q3SSLCVaqRnJ,,9,,apt,,0xe6b117052a39340772791e1318720a574f7fad8fb337bb81b3653c381bf1375b,,,Wallet
Aptos Mainnet Wallet 132 vesting tokens,apt.0x.0xe6b117052a39340772791e1318720a574f7fad8fb337bb81b3653c381bf1375b,,22,,,,,,,Wallet
Aptos Mainnet Wallet 137,lmemMahr22h1iMOGTCQ4,,9,,apt,,0x4c58a38833d6527902c12287c65b83103ae08374e1191ff7fe74b07d43a4dd55,,,Wallet
Aptos Mainnet Wallet 137 Staked Balance,apt.0x.0x4c58a38833d6527902c12287c65b83103ae08374e1191ff7fe74b07d43a4dd55,,22,,,,,,,Wallet
Aptos Mainnet Wallet 138,uKQ3auT3XFDn1qJD8Kyk,,9,,apt,,0x94cb091c5fcba2a168f0b5cf0828405bcce298573a6cc881646210ed5cade8e1,,,Wallet
Aptos Mainnet Wallet 138 vesting tokens,apt.0x.0x94cb091c5fcba2a168f0b5cf0828405bcce298573a6cc881646210ed5cade8e1,,22,,,,,,,Wallet
Aptos Mainnet Wallet 139,eTTW2SaDt6DdZicVhDhy,,9,,apt,,0x81621cf9fa1a44495a5a8f12ad2b44280c8e91292c7f381cb3d5d7c19575bd21,,,Wallet
Aptos Mainnet Wallet 139 vesting tokens,apt.0x.0x81621cf9fa1a44495a5a8f12ad2b44280c8e91292c7f381cb3d5d7c19575bd21,,22,,,,,,,Wallet
Aptos Mainnet Wallet 140,XHS7WPiVYNI6pCBpXJb8,,9,,apt,,0xfd19d127572992c7987f6b0de55d2d83f874fb0097626f2859e01d62bc547728,,,Wallet
Aptos Mainnet Wallet 140 vesting tokens,apt.0x.0xfd19d127572992c7987f6b0de55d2d83f874fb0097626f2859e01d62bc547728,,22,,,,,,,Wallet
Aptos Mainnet Wallet 141,AguVNHjFRhnTIaJ1da3y,,9,,apt,,0x406daf87d651396bed15d8b4b55664a5639e5e1205292e14405307e85f56d37a,,,Wallet
Aptos Mainnet Wallet 144,dQl0EX1Qldxd9y9BWojN,,9,,apt,,0xfadb6980891ab838639e617255324332ba75f58714b2ee281b5984d0819202df,,,Wallet
Aptos Mainnet Wallet 144 vesting tokens,apt.0x1.0x6c84007e93701be49838cde2be39a26f4acfffb3b45d028080649809c8d77952.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 148,HgsJnMOT91G2BRKMdc62,,9,,apt,,0x2eecfeafdec570ebeb171cbec071ebd3eed699af62d3466f282e4f30f7d40c47,,,Wallet
Aptos Mainnet Wallet 148 vesting tokens,apt.0x.0x2eecfeafdec570ebeb171cbec071ebd3eed699af62d3466f282e4f30f7d40c47,,22,,,,,,,Wallet
Aptos Mainnet Wallet 151,NZKUmXCEt5yRMyP3tJ4a,,9,,apt,,0xa7c35b85a72c967777d3fcffd739368af9a2c676e23797c66357769b2cbbf341,,,Wallet
Aptos Mainnet Wallet 151 vesting tokens,apt.0x.0xa7c35b85a72c967777d3fcffd739368af9a2c676e23797c66357769b2cbbf341,,22,,,,,,,Wallet
Aptos Mainnet Wallet 153,ulawXaTKqzO5MVXOKXTt,,9,,apt,,0xaae3dbc92ad472ce5312b6e1f79ec467f37d027ca6064e78475c0f724feea088,,,Wallet
Aptos Mainnet Wallet 154,OyLHYhObnDvupbYlmnU4,,9,,apt,,0x07c0f53feccc51bcb3949243ae730db38eee482631a2ee432b28752f2ec19a3f,,,Wallet
Aptos Mainnet Wallet 154 vesting tokens,apt.0x.0x07c0f53feccc51bcb3949243ae730db38eee482631a2ee432b28752f2ec19a3f,,22,,,,,,,Wallet
Aptos Mainnet Wallet 155,cPqCyqFIiAztN13V0YRH,,9,,apt,,0xe026e8f4d0ce45c7bdc413455a5444dc8ef5dc405720c0bc2b652bcf3678f0b7,,,Wallet
Aptos Mainnet Wallet 155 vesting tokens,apt.0x.0xe026e8f4d0ce45c7bdc413455a5444dc8ef5dc405720c0bc2b652bcf3678f0b7,,22,,,,,,,Wallet
Aptos Mainnet Wallet 157,KfspQXdBeGQNH3PIDJ28,,9,,apt,,0x7581ea8156533ccd8f7fa3b78032fcbcee99e63aa5c9e068914950e2b84da608,,,Wallet
Aptos Mainnet Wallet 157 vesting tokens,apt.0x.0x7581ea8156533ccd8f7fa3b78032fcbcee99e63aa5c9e068914950e2b84da608,,22,,,,,,,Wallet
Aptos Mainnet Wallet 168,VGakkp6FAdqOVZpHOdzS,,9,,apt,,0x035efecb0c07a0ff0367ab01bd38840b796ad4df1959363a0d55495b2bb9fdc2,,,Wallet
Aptos Mainnet Wallet 168 vesting tokens,apt.0x1.0xaa07d109863572d2c7f3850b47fb43e47b457998902e8c64f3b9bc44fe66f148.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 169,B0ZdKhKThHbPY6gFWljz,,9,,apt,,0x8d6aabfbdf88a7199d286c35ef0a92abc6e0aafd5de09c747f19cfcf4b4c5670,,,Wallet
Aptos Mainnet Wallet 169 vesting tokens,apt.0x.0x8d6aabfbdf88a7199d286c35ef0a92abc6e0aafd5de09c747f19cfcf4b4c5670,,22,,,,,,,Wallet
Aptos Mainnet Wallet 17,XQ1aPBwViVXTBsjvbmsW,,9,,apt,,0x82a209a061f02239359417545d804f78fbbe4d3dfe9a7fbf748a21365ed20d9d,,,Wallet
Aptos Mainnet Wallet 17 vesting tokens,apt.0x.0x82a209a061f02239359417545d804f78fbbe4d3dfe9a7fbf748a21365ed20d9d,,22,,,,,,,Wallet
Aptos Mainnet Wallet 171,27XP4gFTm3DtNesJ4CNx,,9,,apt,,0xba417747fc94afde338f5031f556ee5ecec3da795f9e4afa607c724c5fe801bc,,,Wallet
Aptos Mainnet Wallet 171 vesting tokens,apt.0x1.0x6a6783b060213b4892c6da38530ccd274329bcbc4972d37f3ee4dc7b15db1640.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 174,4EZWJpcMgqZQt7BGr5n5,,9,,apt,,0x5cb5ca99d8947a08ee951ed9c994cebd946dacdf4d98441645eca5e6499fb285,,,Wallet
Aptos Mainnet Wallet 174 vesting tokens,apt.0x1.0x4d94fde3604cc27f9c2547b487ab4beaf559ccabe97e278925fa38cfc4ec6765.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 175,veYqNcfnuIw7uuT8Czo5,,9,,apt,,0x1d2cf6993441ae8717a6ef7e29ed7aa07ec3110514354e16e9b633b59bb94a91,,,Wallet
Aptos Mainnet Wallet 175 vesting tokens,apt.0x.0x1d2cf6993441ae8717a6ef7e29ed7aa07ec3110514354e16e9b633b59bb94a91,,22,,,,,,,Wallet
Aptos Mainnet Wallet 176,ONnIOfEffnzxOG2WSFfm,,9,,apt,,0xe016e35ae14826e5831913482c7a625c29a9a2b17e330490ffa2b0515e1710ba,,,Wallet
Aptos Mainnet Wallet 183,V5qLnsAJhwm8OmE0wzcJ,,9,,apt,,0x8a78c7d3a66bb09251622a682f8d1336cf134677487f636c8e815717345784a3,,,Wallet
Aptos Mainnet Wallet 183 Staked Balance,apt.0x.0x8a78c7d3a66bb09251622a682f8d1336cf134677487f636c8e815717345784a3,,22,,,,,,,Wallet
Aptos Mainnet Wallet 184,I4VQBHrHmMX09sqxfC3k,,9,,apt,,0x5b84f643a92ec5259123be474679f28f5f232e9ab178db0de38b79edd28419b7,,,Wallet
Aptos Mainnet Wallet 184 vesting tokens,apt.0x.0x5b84f643a92ec5259123be474679f28f5f232e9ab178db0de38b79edd28419b7,,22,,,,,,,Wallet
Aptos Mainnet Wallet 185,klqdh3DpVWG2iico1LSR,,9,,apt,,0xce7ff9f0b8bbf80b240bd86c389a3bbfe9bb59219da0679680fe2acd6fb85393,,,Wallet
Aptos Mainnet Wallet 185 vesting tokens,apt.0x.0xce7ff9f0b8bbf80b240bd86c389a3bbfe9bb59219da0679680fe2acd6fb85393,,,Wallet
Aptos Mainnet Wallet 186,S91vDvDaXOR6gFn6GVlk,,9,,apt,,0x0756c80f0597fc221fe043d5388949b34151a4efe5753965bbfb0ed7d0be08ea,,,Wallet
Aptos Mainnet Wallet 187,leCoNShXLHNhE8suVoeb,,9,,apt,,0x08ef33d146a95f085fbcf9fd0ed5362de7bc69db5c7d5d9dfd3d8c8acd92b559,,,Wallet
Aptos Mainnet Wallet 188,oLQKUUtffZltmOtluvgp,,9,,apt,,0xc4fce0915e96da42bafa97db7e497896e87763bdd3634486ec4e8a5353183503,,,Wallet
Aptos Mainnet Wallet 189,U6nz76SXRYumyUWDtQGr,,9,,apt,,0x94685b08149f4eae3c75d21287a2f3b74131dae2a0cb7b04adcefca0af644229,,,Wallet
Aptos Mainnet Wallet 19,RBpIy9RxJ3WObsUrmHw7,,9,,apt,,0x9342065552aa86d663bd13b1b43000da75add0f1fa422882d56377a9e6208a3a,,,Wallet
Aptos Mainnet Wallet 19 vesting tokens,apt.0x.0x9342065552aa86d663bd13b1b43000da75add0f1fa422882d56377a9e6208a3a,,22,,,,,,,Wallet
Aptos Mainnet Wallet 190,XAEGgthXTek01dtA69ln,,9,,apt,,0xaa321de84b692666439086bf2bd251f56c9a5d7cc129d8600442093519d8100b,,,Wallet
Aptos Mainnet Wallet 191,sKKmT4VRzdMsY5ZcAPWo,,9,,apt,,0x2fccfed3d745d80b8f72dc5235bec7d82d5fe80c63ab851e4eb22e1829cdcdaa,,,Wallet
Aptos Mainnet Wallet 192,qInei5cPT1TpAoyD9l5Y,,9,,apt,,0x6064d2f4c38b65e9b78fbdf8a80f084159341d47b5e0c192492923326d1bed0a,,,Wallet
Aptos Mainnet Wallet 193,Dk6afYe24zrMg00O6THa,,9,,apt,,0x54ba224e60b095a35322a851adf92e81dd6cb7fd9ee4e2e9a281681501892ec8,,,Wallet
Aptos Mainnet Wallet 194,2Ihcn35ETyr9nNLwTWEq,,9,,apt,,0x96617758ab2df2e871c2248384a43c4427a0a072e789538bea083283d2fef0b5,,,Wallet
Aptos Mainnet Wallet 195,pp2j8FDWzS6rGzXSBmlh,,9,,apt,,0x5870c0c294fb3916567a759937b6ac82732ff35ef284b5563503b9dfc84c8d4b,,,Wallet
Aptos Mainnet Wallet 197,XHYSz1fp2sx0qTVkLuJF,,9,,apt,,0xcd30fbbda98b2aed026772c13e5ed90a7f056b589ef9e78cd96415e1af12451c,,,Wallet
Aptos Mainnet Wallet 198,Ylqp86SMBL5ek9CvAYDd,,9,,apt,,0xdff789994702c4638b0da2c11e2cc69ea63438c2643debfc01a60a8c17e79ff3,,,Wallet
Aptos Mainnet Wallet 198 Staked Balance,apt.0x.0xdff789994702c4638b0da2c11e2cc69ea63438c2643debfc01a60a8c17e79ff3,,22,,,,,,,Wallet
Aptos Mainnet Wallet 199,kjD6UvwdiLiHqWTFqeiD,,9,,apt,,0xb4df284e06648c3fa3bd0c39266f48ba6a97607d04f8a92bd17f658dcc2a1bd3,,,Wallet
Aptos Mainnet Wallet 199 Staked Balance,apt.0x.0xb4df284e06648c3fa3bd0c39266f48ba6a97607d04f8a92bd17f658dcc2a1bd3,,22,,,,,,,Wallet
Aptos Mainnet Wallet 200,sSmL9F53H9kHmeNgEDdB,,9,,apt,,0xccc221485ee530f3981f4beca12f010d2e7bb38d3fe30bfcf7798d99f4aabb33,,,Wallet
Aptos Mainnet Wallet 200 Staked Balance,apt.0x.0xccc221485ee530f3981f4beca12f010d2e7bb38d3fe30bfcf7798d99f4aabb33,,22,,,,,,,Wallet
Aptos Mainnet Wallet 201,snzhxsqfnrK3AHVDwhrV,,9,,apt,,0xf66a130c734a112a5d84c718a1e82a70f2b94ee1195a042cbd5f27081810d7f5,,,Wallet
Aptos Mainnet Wallet 201 Staked Balance,btc.0x.0xf66a130c734a112a5d84c718a1e82a70f2b94ee1195a042cbd5f27081810d7f5,,22,,,,,,,Wallet
Aptos Mainnet Wallet 202,C4T8VC2YtSvMdyxzqIzl,,9,,apt,,0x9931f41f7286e16c227dd7ecdacfa438042faf83e352e4602211eae92bd4871b,,,Wallet
Aptos Mainnet Wallet 202 Staked Balance,apt.0x.0x9931f41f7286e16c227dd7ecdacfa438042faf83e352e4602211eae92bd4871b,,22,,,,,,,Wallet
Aptos Mainnet Wallet 203,xWbNQYYzDftn6Us5NSVU,,9,,apt,,0x48ef004ba16b0a3ea7f04d32a9bef6573169197654c40c81ee46b4dd0ae9f892,,,Wallet
Aptos Mainnet Wallet 204,n1UrvL13BgTIQ0v8TilD,,9,,apt,,0x21b22d459a29cdd663e7bcfd7f1906dd93d8d9fe8099b4c68fe93aadb6250de6,,,Wallet
Aptos Mainnet Wallet 205,EkHaNDeJOO0v1tmpkuYN,,9,,apt,,0x535558440c939163fbff65253a4ce2cf7a16b3144337dbea1f8e0e5cdeb89ffe,,,Wallet
Aptos Mainnet Wallet 206,1ihWs5JFO6d7RXxJBTFb,,9,,apt,,0x215ef071cb38327801144643eaffcf8f9da70b5e0424f6142a83c7377a6e0715,,,Wallet
Aptos Mainnet Wallet 207,5H80hgrr4tfgeqSX9eHK,,9,,apt,,0x5f72f368a64e36af7245b5f0de541de8c8d289622166ae09b72249bf911b841a,,,Wallet
Aptos Mainnet Wallet 208,D8zPjogYPMQxhDyrCztq,,9,,apt,,0x79446f36e69792bad7dc1c2c271b57dceb9132364f425abcba1c91dcc16903a0,,,Wallet
Aptos Mainnet Wallet 209,1ut5UCgDmtKW3ZsWMcAD,,9,,apt,,0x677aa8bad1137f9afd54f19929f071bda27f2bcc23b476d0f24efa81a8c43e36,,,Wallet
Aptos Mainnet Wallet 210,tQEcB0NEkxWmfZVJzgBj,,9,,apt,,0xc5ec99a7823519ea8535adc22c114132342484eae7b71cce18c4a6a3f0b8669a,,,Wallet
Aptos Mainnet Wallet 211,Chyd8GIYvZ6TEkn1mfXb,,9,,apt,,0xf8a0e99649ba484f2e2dd0ea5c2d30b4ef85f77e10bb13222be94afbf0974d7d,,,Wallet
Aptos Mainnet Wallet 212,KsxyG6dyeqnutUB1Do5B,,9,,apt,,0x32e83d55b9e536919837285b2501a93f43862f99297a27ef776154a94c6989a5,,,Wallet
Aptos Mainnet Wallet 213,GHsgCrN6SovM4GbiiYhr,,9,,apt,,0x43f294b8144b1ccc53821084d5e5a8d8e01c0a49304f5103fc5dff74659b3107,,,Wallet
Aptos Mainnet Wallet 214,DH46c7e0sWYWw0x4EZuc,,9,,apt,,0x4a37786aa960a0fa8b5d547182b61d41be313aedc6c8a6a62b2ebc8a9496db5a,,,Wallet
Aptos Mainnet Wallet 216,Eim8Orn7hb2lFjT46K2M,,9,,apt,,0xaa07d109863572d2c7f3850b47fb43e47b457998902e8c64f3b9bc44fe66f148,,,Wallet
Aptos Mainnet Wallet 218,53XYeBT7LsbxSxzaNLm9,,9,,apt,,0xddef941d8d67604f6f8cd7370e199655a749576111cf1e179af702da23dd2b22,,,Wallet
Aptos Mainnet Wallet 218 Staked Balance,apt.0x.0xddef941d8d67604f6f8cd7370e199655a749576111cf1e179af702da23dd2b22,,22,,,,,,,Wallet
Aptos Mainnet Wallet 220,popUHJvGRsvG28BCYOmT,,9,,apt,,0x9189f547224e8136338649c3bc3ea3af5ae81e165c83fb3afcd356b0b00ad4be,,,Wallet
Aptos Mainnet Wallet 221,PGAhHsozztY5rE9pM7LC,,9,,apt,,0xc4599c79e78aa795b14633f035ae9755dee9600927624d11a8064acc6f305486,,,Wallet
Aptos Mainnet Wallet 221 Staked Balance,apt.0x1.0xc4599c79e78aa795b14633f035ae9755dee9600927624d11a8064acc6f305486,,22,,,,,,,Wallet
Aptos Mainnet Wallet 222,Q5H7WtGwUGqovUgn3w3Y,,9,,apt,,0xa91ea5957f7b8dae65e52e28e4bf582bd8a2000a27e9672753ef73decbf7be07,,,Wallet
Aptos Mainnet Wallet 226,TzYJEIN2kJXs2ju451hd,,9,,apt,,0xc23c6b1b157b4ef4da1d97312d0f0d2359914ffd541048744ef4be0a7c61efb9,,,Wallet
Aptos Mainnet Wallet 226 Staked Balance,apt.0x.0xc23c6b1b157b4ef4da1d97312d0f0d2359914ffd541048744ef4be0a7c61efb9,,22,,,,,,,Wallet
Aptos Mainnet Wallet 227,npVzCPzJcxfMC0QQXzJd,,9,,apt,,0x55111beec1a5247ab4577e9870832b9588929fffe3e1b0ecc56eb3da4d1dd8ab,,,Wallet
Aptos Mainnet Wallet 227 Staked Balance,apt.0x.0x55111beec1a5247ab4577e9870832b9588929fffe3e1b0ecc56eb3da4d1dd8ab,,22,,,,,,,Wallet
Aptos Mainnet Wallet 228,XMl89l7iVU6jTdshjif7,,9,,apt,,0x9f2e063d93e00d795e881137d3b7a5e4ee540daae00d610223e349a1ec41a0ae,,,Wallet
Aptos Mainnet Wallet 228 Staked Balance,apt.0x.0x9f2e063d93e00d795e881137d3b7a5e4ee540daae00d610223e349a1ec41a0ae,,22,,,,,,,Wallet
Aptos Mainnet Wallet 23,phkCdYxrXQXhqeTSapNN,,9,,apt,,0x0773be794dd34c38407d9cf8e9f6b382c81ebee4334aec8b4939fcc6cd0e0e33,,,Wallet
Aptos Mainnet Wallet 23 vesting tokens,apt.0x1.0x81f33081a7546b9b3a040f7bfa047ff28a5bb9707072074ad57469b0e885218d.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 230,PRITG6uRLjnQHAhY3ElU,,9,,apt,,0x5c7009064f63e2b82a6999e69e7359bfa129f37249791ce30ef47c4f0c42c66a,,,Wallet
Aptos Mainnet Wallet 230 Staked Balance,apt.0x.0x5c7009064f63e2b82a6999e69e7359bfa129f37249791ce30ef47c4f0c42c66a,,22,,,,,,,Wallet
Aptos Mainnet Wallet 233,RBN4AlLAlEnpEcp6NxdS,,9,,apt,,0x202191439b23bca6bfce51597124291f951daccd60fa7c678d78858c7612d3e5,,,Wallet
Aptos Mainnet Wallet 236,X556mO2nliPZj93oYkcX,,9,,apt,,0x4d94fde3604cc27f9c2547b487ab4beaf559ccabe97e278925fa38cfc4ec6765,,,Wallet
Aptos Mainnet Wallet 236 Staked Balance,apt.0x.0x4d94fde3604cc27f9c2547b487ab4beaf559ccabe97e278925fa38cfc4ec6765,,22,,,,,,,Wallet
Aptos Mainnet Wallet 238,qwEeKX46vVRG8hcif9XK,,9,,apt,,0xf74922a3ef2331f5621959aad09a4067bead090525aae564024554f2f93f4d18,,,Wallet
Aptos Mainnet Wallet 24,nm3X9BPO99GczbMoV0x5,,9,,apt,,0xc65d3d252f87d4244048771c803ae5247bd349822a7df66893806441e1b4e90f,,,Wallet
Aptos Mainnet Wallet 24 vesting tokens,apt.0x1.0x55111beec1a5247ab4577e9870832b9588929fffe3e1b0ecc56eb3da4d1dd8ab.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 243,5YlftEtpTEl7of8mCCAo,,9,,apt,,0x072c78c9ce114fbb9acadb0ac1e235cd9fc0fc4c3ee618d4416818c43ecc01c9,,,Wallet
Aptos Mainnet Wallet 245,R6XpFCtrAhPmtWBDKIBG,,9,,apt,,0xb1fe5517c3a927978a9e50b89a4f582d11bf8f987ff77630723a9c49960db018,,,Wallet
Aptos Mainnet Wallet 246,bJaI10BiLzdwOeYZw9qm,,9,,apt,,0xbf4eae0d614b8a7207cd0f8df9cc3fb5a3663616ec76ab397d82d29de712f693,,,Wallet
Aptos Mainnet Wallet 246 Staked Balance,apt.0x.0xbf4eae0d614b8a7207cd0f8df9cc3fb5a3663616ec76ab397d82d29de712f693,,22,,,,,,,Wallet
Aptos Mainnet Wallet 247,1VqlcNX0BEloINHFU2P3,,9,,apt,,0x67575e0d56a26a1a6dc6005a7b0c4647b2b5c78a2234aac52cba2bfc713ecf0d,,,Wallet
Aptos Mainnet Wallet 248,WWRi7MZrNfJHk56mEKjP,,9,,apt,,0x8b2b0f85b2c6d913f97f0ad5180c6f8a295c08b86ed7d07a63545b97c4b00355,,,Wallet
Aptos Mainnet Wallet 249,EEFuDq1KirTxb91UNoKD,,9,,apt,,0x6c84007e93701be49838cde2be39a26f4acfffb3b45d028080649809c8d77952,,,Wallet
Aptos Mainnet Wallet 250,W0WQMYM4vbPq0Qd2skj2,,9,,apt,,0x6a6783b060213b4892c6da38530ccd274329bcbc4972d37f3ee4dc7b15db1640,,,Wallet
Aptos Mainnet Wallet 250 Staked Balance,apt.0x.0x6a6783b060213b4892c6da38530ccd274329bcbc4972d37f3ee4dc7b15db1640,,22,,,,,,,Wallet
Aptos Mainnet Wallet 251,N0nvu806NetCOTiVDnrC,,9,,apt,,0x38e1b87887946977b5170a299bbaba2e2b728c5ef96847a4482973706c810112,,,Wallet
Aptos Mainnet Wallet 254,3y5yadJgCl8QpaoRhsQ2,,9,,apt,,0x0d24ecb979d3031f198f0e76ed22894c1b8f8af5ab944f5659c6f0bcc628f10a,,,Wallet
Aptos Mainnet Wallet 256,fdMrAME5k4Sb2cBmAIKy,,9,,apt,,0x81f33081a7546b9b3a040f7bfa047ff28a5bb9707072074ad57469b0e885218d,,,Wallet
Aptos Mainnet Wallet 257,SYGkGNAItYRPdwL6MD9m,,9,,apt,,0x74b0c27c7d3b89b22962f6a609ef9a11cde10756045273163f35175e7cb164f5,,,Wallet
Aptos Mainnet Wallet 257 Staked Balance,apt.0x.0x74b0c27c7d3b89b22962f6a609ef9a11cde10756045273163f35175e7cb164f5,,22,,,,,,,Wallet
Aptos Mainnet Wallet 258,JLFl98I13MEb0xZDJNJf,,9,,apt,,0x53496ba0c3974434add4bea19ba2dc5aa63713dc30b566ff5062d94357d8b348,,,Wallet
Aptos Mainnet Wallet 259,wH4cxVzsfirP0WPC6kfK,,9,,apt,,0x9201d69100aaa13f6ae3e2f7db87f08cb25c43f6134bd62855970e2f13e81898,,,Wallet
Aptos Mainnet Wallet 260,cdLuXe6dnLqGUx65jbho,,9,,apt,,0xe87747b6faa3f5095341714fba8edf6b4b88489cdf33e1192fe23c8fb3509dc6,,,Wallet
Aptos Mainnet Wallet 264,exGnYAGWLS7dUFDSSHsg,,9,,apt,,0xa32e6f8dc6747b53d75e57e79b539aa641711604aaedac98ab84a73f30c7617a,,,Wallet
Aptos Mainnet Wallet 266,Jt0xc4l1JoVfHRLibm0V,,9,,apt,,0x1df9fc0f3908ddc1025c91d774ba7954404ae710a3ebc4d25bc7bf7fcb26ffb4,,,Wallet
Aptos Mainnet Wallet 267,RG6U1EwUuarpkrWz3LAe,,9,,apt,,0xed2c3d0826094963df0ee80c3b28555e3024f5ecf6b9beb88f26379fa19b3b7f,,,Wallet
Aptos Mainnet Wallet 268,7UAer4QIuzQ4I1obWPsJ,,9,,apt,,0x0bb4d4cea83abc7acef52cb4e167805be446d647b91989c6e0b4f71c45e54baa,,,Wallet
Aptos Mainnet Wallet 301,TriA1hvDHaWVuyxNdUxF,,9,,apt,,0xaaa9c5fb3b4855e1569321041febcc1146b44af3f08893d4ce41846cc7e25645,,,Wallet
Aptos Mainnet Wallet 303,kVphc396apWY2XoKAePz,,9,,apt,,0x5711fd997e7ad78dbbf1e8cb0b89af50f4f013d6114afb2fd0c520fa763f68e2,,,Wallet
Aptos Mainnet Wallet 306,wDojtDI52MisSPv20x0R,,9,,apt,,0xb64719986e834691b58d2c5ee923a367ffcb80eed93e8b71c5e0b5fe189fac49,,,Wallet
Aptos Mainnet Wallet 306 Staked Balance,apt.0x.0xb64719986e834691b58d2c5ee923a367ffcb80eed93e8b71c5e0b5fe189fac49,,22,,,,,,,Wallet
Aptos Mainnet Wallet 307,GkXp8V81AnWXDjnNckLs,,9,,apt,,0x702ebda8da252a8771b9cfa7d5cf837549ddb6d4863a875a114298649d9faaec,,,Wallet
Aptos Mainnet Wallet 308,OGtgUeLQgZJlWTQkooRf,,9,,apt,,0xabc5ddee336de6fd180a987ddecfa7e6d0f9399741f9f08f0b6789548e92f6ef,,,Wallet
Aptos Mainnet Wallet 308 Staked Balance,apt.0x.0xabc5ddee336de6fd180a987ddecfa7e6d0f9399741f9f08f0b6789548e92f6ef,,22,,,,,,,Wallet
Aptos Mainnet Wallet 31,t1JfY0gF7Qgo4GEngOq3,,9,,apt,,0xf949e46b05a1414ec6b5de673ce331e4dd6e351e43dc2b70f2e3639d468eba6f,,,Wallet
Aptos Mainnet Wallet 31 vesting tokens,apt.0x1.0x74b0c27c7d3b89b22962f6a609ef9a11cde10756045273163f35175e7cb164f5.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 32,O4FyjWLIgYW3TI6MAqt7,,9,,apt,,0x834b4d54d30d3c58a5f791cd4bc80ce5919c062575f8b98c1b671b1a222e29ac,,,Wallet
Aptos Mainnet Wallet 36,EHaqhjJ38yf5Q5mO51py,,9,,apt,,0x6171a66ef37f2c9f5065142b01d8139409453b29753fe19cb0356be08c930751,,,Wallet
Aptos Mainnet Wallet 36 vesting tokens,apt.0x1.0xbf4eae0d614b8a7207cd0f8df9cc3fb5a3663616ec76ab397d82d29de712f693.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 37,tfI9FaLn8PvI74YlUrDJ,,9,,apt,,0x065e1ec4bfffd4592379e729e5a595254bda27cc3521889e1770aa3370cacd18,,,Wallet
Aptos Mainnet Wallet 39,OYDc0YG4DC7VXbcL3TjE,,9,,apt,,0x1720fe518f0a2573a61704de1d07f430df87a1549e70697c54d56c0445ee88f7,,,Wallet
Aptos Mainnet Wallet 48,OT6fgNzWLTZTb3SWYhth,,9,,apt,,0xb69f4f7bb52ed7b111afe95d6492bb5addeac81fa734f087f5b6315981ac9f90,,,Wallet
Aptos Mainnet Wallet 50,PRQKGLlBTH00ttqfyWLb,,9,,apt,,0xb71a9c7dbce47be1706566aeb2b47d60f24b52aec039bd78e58fee77a71bece4,,,Wallet
Aptos Mainnet Wallet 50 Staked Balance,apt.0x.0xb71a9c7dbce47be1706566aeb2b47d60f24b52aec039bd78e58fee77a71bece4,,22,,,,,,,Wallet
Aptos Mainnet Wallet 52,0VtpncYrsq2FBt7Mxj0E,,9,,apt,,0x258bc02e81cc57b7e3383eb5866513428257fefde8e69684215add52aa0abd8b,,,Wallet
Aptos Mainnet Wallet 52 Staked Balance,apt.0x.0x258bc02e81cc57b7e3383eb5866513428257fefde8e69684215add52aa0abd8b,,22,,,,,,,Wallet
Aptos Mainnet Wallet 53,xrEzpCQYGpErpwo3QvkY,,9,,apt,,0x0bddf6990a52fce1c29f69b6196150143e9ac44e4984bbc52741e60f422817da,,,Wallet
Aptos Mainnet Wallet 53 vesting tokens,apt.0x1.0x9f2e063d93e00d795e881137d3b7a5e4ee540daae00d610223e349a1ec41a0ae.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 55,YrFFWWzoxRIdLwnoF6kG,,9,,apt,,0x6e745e1fec530a6e8cbb37636591da99da53114dd6dd63732d3d6b0fe3d3a6ef,,,Wallet
Aptos Mainnet Wallet 55 vesting tokens,apt.0x.0x6e745e1fec530a6e8cbb37636591da99da53114dd6dd63732d3d6b0fe3d3a6ef,,22,,,,,,,Wallet
Aptos Mainnet Wallet 58,CTPXwy52KE7P7899MujJ,,9,,apt,,0xee86edd0102ba974725bce23b126d922aaf76d3e53f715a842aaffa301483ed3,,,Wallet
Aptos Mainnet Wallet 58 Vesting Tokens,apt.0x.0xee86edd0102ba974725bce23b126d922aaf76d3e53f715a842aaffa301483ed3,,22,,,,,,,Wallet
Aptos Mainnet Wallet 6,wNShRpwkXxyAOYWoyLfc,,9,,apt,,0x1af1823ca71a9cbd37005e7a4b4b3815fb26ce25cc53ec633aadd7ebade11dc2,,,Wallet
Aptos Mainnet Wallet 6 vesting tokens,apt.0x1.0x5c7009064f63e2b82a6999e69e7359bfa129f37249791ce30ef47c4f0c42c66a.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 62,7Fjt4SGM0vcyFeWHJKhY,,9,,apt,,0xc017e802c25f519f26209785a88c2688b2b75caeca3624f12fdf9274a02874d5,,,Wallet
Aptos Mainnet Wallet 62 vesting tokens,apt.0x.0xc017e802c25f519f26209785a88c2688b2b75caeca3624f12fdf9274a02874d5,,22,,,,,,,Wallet
Aptos Mainnet Wallet 65,Z9E32MVE2ffU0r6r1G8U,,9,,apt,,0x7b7ebee202201e23f3d443d97d8884a83dd5933be59e033ce8273dd82b66af1a,,,Wallet
Aptos Mainnet Wallet 65 vesting tokens,apt.0x1.0xc23c6b1b157b4ef4da1d97312d0f0d2359914ffd541048744ef4be0a7c61efb9.382436115963136,,22,,,,,,,Wallet
Aptos Mainnet Wallet 66,vBEKRGkNIi0Fqx0v02Gx,,9,,apt,,0xd90a51dc740b22ac487139962e6e0e0c2b694b98af01ddc39c4ae46d62ae3e9c,,,Wallet
Aptos Mainnet Wallet 66 Staked Balance,apt.0x.0xd90a51dc740b22ac487139962e6e0e0c2b694b98af01ddc39c4ae46d62ae3e9c,,22,,,,,,,Wallet
Aptos Mainnet Wallet 67,DTKmVvZuSprWq5wJZIJn,,9,,apt,,0xe96d0792cd62b99f434e542c5dd9b4e146e71bad5ccbff65c51a350f9972d0fe,,,Wallet
Aptos Mainnet Wallet 70,lEvex6f7Q66tlMSOOMZV,,9,,apt,,0x8d4184a18addf3a54ee2d8c120e9b1de5e929f22057b87b9ef2abee38c6784bd,,,Wallet
Aptos Mainnet Wallet 70 vesting tokens,apt.0x.0x8d4184a18addf3a54ee2d8c120e9b1de5e929f22057b87b9ef2abee38c6784bd,,22,,,,,,,Wallet
Aptos Mainnet Wallet 71,B1vKzo2W0ASP70Ff1tOl,,9,,apt,,0xdd79bb077b5480786e4aad7823c2f56368d7c7cdb4350d0cafa735939c1c2d4c,,,Wallet
Aptos Mainnet Wallet 71 vesting tokens,apt.0x.0xdd79bb077b5480786e4aad7823c2f56368d7c7cdb4350d0cafa735939c1c2d4c,,22,,,,,,,Wallet
Aptos Mainnet Wallet 73,qT07kDUZ6AoW1J8EiAg6,,9,,apt,,0x9b95702596a45d806ae6ef2a17b955e140c79fed84590ea2aa7f0fdc3440dd00,,,Wallet
Aptos Mainnet Wallet 73 Staked Balance,apt.0x.0x9b95702596a45d806ae6ef2a17b955e140c79fed84590ea2aa7f0fdc3440dd00,,22,,,,,,,Wallet
Aptos Mainnet Wallet 74,r2pdnZUMCnow9TEwK4DM,,9,,apt,,0x4b705711e08994790da690388ad07f5391f7258aa47af41c7e5545cd28c4a4ab,,,Wallet
Aptos Mainnet Wallet 75,nqZ4Kqtaxy3XPM7VEX9k,,9,,apt,,0x75d82b3fb50875a6858311ff7686b4a5062ed1547ca615c664b6e5b8c4cad399,,,Wallet
Aptos Mainnet Wallet 75 vesting tokens,apt.0x.0x75d82b3fb50875a6858311ff7686b4a5062ed1547ca615c664b6e5b8c4cad399,,22,,,,,,,Wallet
Aptos Mainnet Wallet 76,6DZAvMP1tsFmZUOnDV4R,,9,,apt,,0xb75ba0117fd363a54dc976636d003958bf36124cc9bfc6f8e8a953f053ab14ca,,,Wallet
Aptos Mainnet Wallet 76 Staked Balance,apt.0x.0xb75ba0117fd363a54dc976636d003958bf36124cc9bfc6f8e8a953f053ab14ca,,22,,,,,,,Wallet
Aptos Mainnet Wallet 78,bpfioPNYt9uaoLOVV2us,,9,,apt,,0xd6d70afbe79d002f1ad135025deccd5a8257c61a4725c8b69291929173717bbb,,,Wallet
Aptos Mainnet Wallet 78 vesting tokens,apt.0x.0xd6d70afbe79d002f1ad135025deccd5a8257c61a4725c8b69291929173717bbb,,22,,,,,,,Wallet
Aptos Mainnet Wallet 84,p8JbpIOyhT3EebkDwTU7,,9,,apt,,0x8a2b9c9815d07e049dab7b02ad6104bff5adb539948b731ceaf38f8c6f151bf4,,,Wallet
Aptos Mainnet Wallet 84 vesting tokens,apt.0x.0x8a2b9c9815d07e049dab7b02ad6104bff5adb539948b731ceaf38f8c6f151bf4,,22,,,,,,,Wallet
Aptos Mainnet Wallet 85,1SB5vuZxsyOGppgE697W,,9,,apt,,0x9503582321f1ddf75ee5bce7c6a27f3ad105c2f4b6426367c662e93f46cd4f0c,,,Wallet
Aptos Mainnet Wallet 85 vesting tokens,apt.0x.0x9503582321f1ddf75ee5bce7c6a27f3ad105c2f4b6426367c662e93f46cd4f0c,,22,,,,,,,Wallet
Aptos Mainnet Wallet 87,Vatpx0F6a5WxoJjni4ds,,9,,apt,,0x9ff36d0476bd923f29e43fae2c251d5a02c3532e4dde18270ff2882378d62226,,,Wallet
Aptos Mainnet Wallet 88,uRWE8WZQDlD6bUMBAzVO,,9,,apt,,0x28007cdf67281f26c30bccb7651c582880fff7007bb83fc85a3e080213e7b3ae,,,Wallet
Aptos Mainnet Wallet 88 vesting tokens,apt.0x.0x28007cdf67281f26c30bccb7651c582880fff7007bb83fc85a3e080213e7b3ae,,22,,,,,,,Wallet
Aptos Mainnet Wallet 90,zKvo8JPVoWoJBXiIEeAL,,9,,apt,,0x887dbc66257a99518b98ffc0b86ab84dd9974aea1667498623540d5bbb66bfba,,,Wallet
Aptos Mainnet Wallet 90 Staked Balance,apt.0x.0x887dbc66257a99518b98ffc0b86ab84dd9974aea1667498623540d5bbb66bfba,,22,,,,,,,Wallet
Aptos Mainnet Wallet 93,gvL5q1NO1BIVeVRHOeHy,,9,,apt,,0x64b21481a432f9a9afdc134bad91e8a3361556db8fdb618978780b201ca0c913,,,Wallet
Aptos Mainnet Wallet 93 vesting tokens,apt.0x.0x64b21481a432f9a9afdc134bad91e8a3361556db8fdb618978780b201ca0c913,,22,,,,,,,Wallet
Aptos Mainnet Wallet 97,STlPOXUxicCm2WHyfCHo,,9,,apt,,0x256724e94b026171601ff9d16fb5eb8ef08b10b7b19e374e017653db84816787,,,Wallet
Aptos Mainnet Wallet 97 vesting tokens,apt.0x.0x256724e94b026171601ff9d16fb5eb8ef08b10b7b19e374e017653db84816787,,22,,,,,,,Wallet
Aptos Mainnet Wallet 98,BOF5bePOCHApT6IuHJ88,,9,,apt,,0x40236e3f4ee2f7e1b15795edc10d8bf7e07aad93ae94051a3efe7a95efef02f7,,,Wallet
Aptos Mainnet Wallet 98 vesting tokens,apt.0x.0x40236e3f4ee2f7e1b15795edc10d8bf7e07aad93ae94051a3efe7a95efef02f7,,22,,,,,,,Wallet
Coinbase Aptos Wallet 1,7qQHlJ7Dzc49v4uHQsAi,,9,,apt,,0x2a3951ca94ae2eec32d583e5b2fad01d6509bddf56228e91539f82ec379bd4f9,,,Wallet
Coinbase Aptos Wallet 2,f4FTR9bCn5bhMuPNQm6Q,,9,,apt,,0xb0662deb05232b5cc11a21c736d1deb272c48f8e693c91ec9b8845df223e4642,,,Wallet
Coinbase Aptos Wallet 2 Staked Balance,apt.0x.0xb0662deb05232b5cc11a21c736d1deb272c48f8e693c91ec9b8845df223e4642,,22,,,,,,,Wallet
Coinbase Aptos Wallet 3,DTosEdzIoFbpROFfVzXG,,9,,apt,,0xb151002e448a56fc775973e3d49809e996701694746362ec9d461bff98179061,,,Wallet
Coinbase Aptos Wallet 3 Staked Balance,apt.0xb151002e448a56fc775973e3d49809e996701694746362ec9d461bff98179061.0x,,22,,,,,,,Wallet
Coinbase Aptos Wallet 4,o6ZhaPhkCIZC9A60OW9L,,9,,apt,,0x9876c642821cc6b7b8516d442758290b5b1a92c8f5ab9a215a767f198ea5ff0c,,,Wallet
Coinbase Aptos Wallet 4 Staked Balance,apt.0x.0x9876c642821cc6b7b8516d442758290b5b1a92c8f5ab9a215a767f198ea5ff0c,,22,,,,,,,Wallet
Coinbase Aptos Wallet 6,lUH70OHYr0WEQEkSpLAg,,9,,apt,,0x688e90d6b0f078655429e640627d25647265f1d4903ba994812fa3199634bb17,,,Wallet
Coinbase Aptos Wallet 7,GJuYbvTVgFOWhg2pSjLq,,9,,apt,,0x3ba7c9bfd9cda914151a9dad1ad302de343ee210ad35983be70dc53d2e335b16,,,Wallet
Coinbase Aptos Wallet 8,Yr3axPmIXUUuCRuUnKFb,,9,,apt,,0x221f0772ec033abba7f6ead240a9752623c8b345a1f26c614d6adaa51d12188b,,,Wallet
Coinbase Aptos Wallet 9,3Jgo91nL90v2uIUAfvel,,9,,apt,,0x02b60ce6f2dfccb5f14fa881d173c60abc282ff39e5467f78c573ae3eebe8365,,,Wallet
Coinbase Corporate Wallet 1,0zonIEQcoaazfVNbNoTa,,9,,apt,,0x86114c4470870bc3db41d0f6bccfff0e70c7fdc3346c5fa6b3fd0046a9347503,,,Wallet
Coinbase Corporate Wallet 1 Staked Balance,apt.0x.0x86114c4470870bc3db41d0f6bccfff0e70c7fdc3346c5fa6b3fd0046a9347503,,22,,,,,,,Wallet
Coinbase Corporate Wallet 2,InqnKfiCqdSW5PYtvBXA,,9,,apt,,0xee482a204dcb86861680765377c5ec2c4b204110e9409f4da5dce9de5885b58c,,,Wallet
Coinbase Corporate Wallet 2 Staked Balance,apt.0x.0xee482a204dcb86861680765377c5ec2c4b204110e9409f4da5dce9de5885b58c,,22,,,,,,,Wallet
Coinbase Corporate Wallet 3,4zxS9r3jb4vPI6ZelImD,,9,,apt,,0x3aa48956d35b5009736d3e244d1a4efd291f18f7a578e7640d7ab1efb6648281,,,Wallet
Coinbase Corporate Wallet 3 Staked Balance,apt.0x.0x3aa48956d35b5009736d3e244d1a4efd291f18f7a578e7640d7ab1efb6648281,,22,,,,,,,Wallet
Coinbase Corporate Wallet 4,B5moeDWB8TANuCcJAUwX,,9,,apt,,0xea171c55d235315a70b80e6bc9c1aa5d4932e58c70d74fd4e343806b81e55aa5,,,Wallet
Coinbase Corporate Wallet 4 Staked Balance,apt.0x.0xea171c55d235315a70b80e6bc9c1aa5d4932e58c70d74fd4e343806b81e55aa5,,22,,,,,,,Wallet
Coinbase Corporate Wallet 5,zlbM8xPQ4MZd1pPVegwk,,9,,apt,,0xbdceea016b1f23fef28750d1b7358100b4118fd1768bfacf2a78693dcd9f9168,,,Wallet
Coinbase Corporate Wallet 5 Staked Balance,apt.0x.0xbdceea016b1f23fef28750d1b7358100b4118fd1768bfacf2a78693dcd9f9168,,22,,,,,,,Wallet
Coinbase Corporate Wallet 6,jxj3yaw42KqwMrS6HDXT,,9,,apt,,0xeb9f4f25e31230d39f5b07ca5e3bf72451afef1e2084a14ec48ac7def075cc22,,,Wallet
Coinbase Corporate Wallet 6 Staked Balance,apt.0x.0xeb9f4f25e31230d39f5b07ca5e3bf72451afef1e2084a14ec48ac7def075cc22,,22,,,,,,,Wallet
Coinbase Corporate Wallet 7,p2lPlnx5UcDL4WMvhPre,,9,,apt,,0xe89a3816fd4ba1f15eef69d8281b82482bf6ec077001c0b7ed5aae4f42d55ceb,,,Wallet
Coinbase Corporate Wallet 7 Staked Balance,apt.0x.0xe89a3816fd4ba1f15eef69d8281b82482bf6ec077001c0b7ed5aae4f42d55ceb,,22,,,,,,,Wallet
"""

# Load Wallets List into DataFrame
wallets_df = pd.read_csv(io.StringIO(wallets_csv))

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV
        df = pd.read_csv(uploaded_file)
        
        # Validate required columns
        required_columns = ['Month', 'Destination Wallet', 'Total Asset Quantity', 'Total Value (USD)']
        if not all(col in df.columns for col in required_columns):
            st.error("Uploaded CSV must contain columns: Month, Destination Wallet, Total Asset Quantity, Total Value (USD)")
            st.stop()
        
        # Display the uploaded data
        st.subheader("Uploaded Data")
        st.dataframe(df)
        
        # Create output DataFrame with required columns
        output_df = pd.DataFrame(columns=[
            'id', 'remoteContactId', 'amount', 'amountTicker', 'cost', 'costTicker',
            'fee', 'feeTicker', 'time', 'blockchainId', 'memo', 'transactionType',
            'accountId', 'contactId', 'categoryId', 'taxExempt', 'tradeId',
            'description', 'fromAddress', 'toAddress', 'groupId'
        ])
        
        # Track missing staking wallets to avoid duplicate alerts
        missing_wallets = set()
        
        # Populate output DataFrame
        output_data = []
        for idx, row in df.iterrows():
            # Generate unique ID
            unique_id = str(uuid.uuid4())
            
            # Format time: 12:00pm on last day of the month
            month_str = row['Month']
            try:
                date_obj = datetime.strptime(month_str, '%Y-%m')
                last_day = monthrange(date_obj.year, date_obj.month)[1]
                time_obj = datetime(date_obj.year, date_obj.month, last_day, 12, 0)
                formatted_time = time_obj.strftime('%m/%d/%y %I:%M%p').lower()
                # For blockchainId, get MMDDYY
                mmddyy = time_obj.strftime('%m%d%y')
            except ValueError:
                st.warning(f"Invalid Month format in row {idx+1}: {month_str}. Skipping row.")
                continue
            
            # Get accountId from Wallets List using partial match
            destination_wallet = row['Destination Wallet']
            # Extract wallet number (e.g., '52' from 'Aptos Mainnet Wallet 52')
            match = re.search(r'\b(\d+)\b', destination_wallet)
            wallet_number = match.group(1) if match else None
            
            account_id = ''
            if wallet_number:
                # Search for partial match: "Wallet <number> Staked Balance"
                target_pattern = rf'Wallet\s*{wallet_number}\s*Staked\s*Balance'
                matching_rows = wallets_df[wallets_df['name'].str.contains(target_pattern, case=False, regex=True)]
                if not matching_rows.empty:
                    account_id = matching_rows.iloc[0]['id']
                else:
                    if destination_wallet not in missing_wallets:
                        st.warning(f"{destination_wallet} is missing a staking wallet")
                        missing_wallets.add(destination_wallet)
            else:
                if destination_wallet not in missing_wallets:
                    st.warning(f"{destination_wallet} is missing a staking wallet")
                    missing_wallets.add(destination_wallet)
            
            # Construct blockchainId
            blockchain_id = f"{account_id}.stakingrewards.{mmddyy}" if account_id else f"stakingrewards.{mmddyy}"
            
            output_data.append({
                'id': unique_id,
                'remoteContactId': '',
                'amount': row['Total Asset Quantity'],
                'amountTicker': 'APT',
                'cost': row['Total Value (USD)'],
                'costTicker': 'USD',
                'fee': '',
                'feeTicker': '',
                'time': formatted_time,
                'blockchainId': blockchain_id,
                'memo': '',
                'transactionType': 'deposit',
                'accountId': account_id,
                'contactId': 'nFc4OUI5w6wSa6zFKQVj.526',
                'categoryId': 'nFc4OUI5w6wSa6zFKQVj.265',
                'taxExempt': 'FALSE',
                'tradeId': '',
                'description': 'staking rewards import',
                'fromAddress': '',
                'toAddress': '',
                'groupId': ''
            })
        
        if not output_data:
            st.error("No valid rows processed. Please check the Month column format (e.g., '2025-01').")
            st.stop()
        
        output_df = pd.DataFrame(output_data)
        
        # Display the processed data
        st.subheader("Processed Data (Output Format)")
        st.dataframe(output_df)
        
        # Convert output data to CSV
        csv_buffer = io.StringIO()
        output_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Provide download button for the new CSV
        st.subheader("Download Processed CSV")
        st.download_button(
            label="Download Transaction CSV",
            data=csv_data,
            file_name="processed_transactions.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload a CSV file to proceed.")
