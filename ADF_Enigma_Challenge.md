## Operation Enigma Write up

One challenge particularly piqued my interest. I really like cryptography, so this one had my name on it. Some background...

#### Name of Challenge:  Operation Enigma

#### Description:

We have intercepted two messages from Marshal of the Russian Federation, Barry.  We need you to work out what he is sharing with is Army General.

### Cyphertext Samples

1.
```
Iptufyl,

S jtwc didj spdspp jgekk lvg vu djrw ibrzlp zyg ekeb ztafayg. Kw'h tfjz u cgqit gakhm lo udwk nnxjduxkh, rmg G fyswwa ck znpa v rfofzh or pzgyatj ec tcqzkco qbxdkjyzngci tvn qlto zdbgmqjnql mfe beyoxzb.

NMJO{dpztldkwrm}

Zqvf mhf tzyndkvaw qnn zhbi aqeya ju wntpusmhzv, ykb sq'x axovxte dyz xtbcawcezsg drfa xu seam eyvabjyv qmo dnatibzrya. Tcxg muqpvoma ydb avrg s tabrvvia zlrcma sx bypmncxitmv, bsi J'e lxwwschu osi yvg idtmucx nt'rd fublrr.

Xt tp xypx ykgyzmx, C jryt gsuvzdz ka fmr zfuglydmu aexjwo yy umh zunrvluafg tyf jms bkfjma bmcjhusjvmt vrrb nesnm. Ctkuax gwwk uclz otp rvy pmryxp ue or rfsbiaiu.

Qqtwvzwpg,

Jjtzh
```

2.

```
Iptufyl,

S vpvqd jfgl yfscbn apgbc mjx cnum vqf vj hyjc abkwuqh. Aq'x cphg swovemred ewxnyyheo xmxk U vqrwz mbj hb srg zwuju. Pkdu extyubdoku iri migwbhq pltg psos m eamjgh ee wnctm bv ra kqsg.

ZXFM{qwnadbraur}

Aw krhdy zx vsbteaosh ikt ewc, umwy cparytjp aoq wpac e npjqpv eb qokxxebv nhy nfgiydkryms. H nomaewk pru eerutrt vs'at cjkre naevxgop slu mrn igapqdux du'jv xzfwfvb.

Eategyb tfbxk, E'o rftpavl hojzc mim brooafmhor mke emxhto olzlnytsfrz skkp zzg rpxypu rmtxu qby jz. Ejpu bqkhlvzmsv srhzq kxx yhjbo vy xz, boe V'o czjbcifs qzu aivi smkdhnemfd exgamzq.

Fpanbmnud,

Zuljh
```


### Initial analysis. 

My 1st task was to figure out what kind of cypher this was. Immediately, I noticed the lack of 5 letter groups and luck would have it have it, punctuation was included. Solving this cypher became infinitely more easy. 

Normally, the beginning is where I start. However the CTF challenge description led me to skip to the last grouping. My assumption was this group was Barry. The letters added up. Quickly though I noticed the 1st group was the same in both cyphertexts. I returned to Barry. A quirk, I like quirks when it comes to solving cryptography, they help to make encryption algorithm identification far easier. 

My mind turned to letter frequency. It quickly became obvious this was a stream cypher. Which would make frequency analysis not useful for this challenge. All was not lost. I had a crib, known-plaintext attack was a possibility. 

Around this time... I was starting to zone out.  Lack of sleep was catching up with me. I wanted to solve this challenge. For some inexplicable reason my mind turned to enigma. The starting group, which turned out to be Comrade reminded me of "Wetter" of Bletchly Park fame. Though, the signing of the cryptotexts with Barry is more accurate of a comparison. This cyphertext screamed enigma. Crib, stream cypher and the fact it was a CTF... led me to conclude enigma was used. 

### Solving. 

I went looking for an enigma simulator online. I thought I had already written a script to solve enigma (but I was tired and running quickly out of energy and time). But I knew the next step was to find the settings of the machine. I was running out of time to pull together a script for this particular crypto text. So I found a cool online simulator and played around with settings. I didn't have too many clues at this point to the settings.  I stumbled on a site that would solve the crypto in one fell swoop by default. [Enigma Machine Simulator Online - DenCode](https://dencode.com/en/cipher/enigma) . It found the correct settings rather quickly and nabbed me the flag.  It was an Enigma 1, which latter I noticed was a tip the organisers gave. 

#### The flag: 
FLAG{impressive}
