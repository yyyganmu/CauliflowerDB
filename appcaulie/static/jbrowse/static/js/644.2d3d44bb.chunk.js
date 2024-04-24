"use strict";(self.webpackChunk_jbrowse_web=self.webpackChunk_jbrowse_web||[]).push([[644],{19068:function(e,t,n){n.r(t),n.d(t,{default:function(){return j}});var r=n(33028),a=n(59740),u=n(68079),s=n(41361),c=n(32723),i=n(34795),o=n(9249),f=n(87371),l=n(45754),p=n(13820),m=n(2646),h=n(23995),v=n(32145),d=n(93824),g=n(99836),b=n(16959),y=n(19390),Z=n(93069),x=n(95058),k=n(95802),w=y.tr.getMismatches,q=function(e){(0,l.Z)(n,e);var t=(0,p.Z)(n);function n(){return(0,o.Z)(this,n),t.apply(this,arguments)}return(0,f.Z)(n,[{key:"get",value:function(e){return"mismatches"===e?w(this.get("CIGAR")):(0,Z.Z)((0,x.Z)(n.prototype),"get",this).call(this,e)}}]),n}(k.SimpleFeature),N=n(44922),A=n(46840),C=n(96234);function M(e){for(var t={},n=0;n<e.length;n++){var r=e[n],a=r.qname+"-"+r.tname;t[a]||(t[a]={quals:[],len:[]}),t[a].quals.push(r.extra.mappingQual),t[a].len.push(r.extra.blockLen||1)}for(var u=Object.fromEntries(Object.entries(t).map((function(e){var t=(0,C.Z)(e,2),n=t[0],r=t[1];return[n,D((0,N.$R)(r.quals,r.len))]}))),s=0;s<e.length;s++){var c=e[s],i=c.qname+"-"+c.tname;c.extra.meanScore=u[i]}for(var o=1e4,f=0,l=0;l<e.length;l++){var p=e[l];o=Math.min(p.extra.meanScore||0,o),f=Math.max(p.extra.meanScore||0,f)}for(var m=0;m<e.length;m++){var h=e[m],v=h.extra.meanScore||0;h.extra.meanScore=(v-o)/(f-o)}return e}function D(e){var t=e.reduce((function(e,t){var n=(0,C.Z)(e,2),r=n[0],a=n[1],u=(0,C.Z)(t,2),s=u[0],c=u[1];return[r+s*c,a+c]}),[0,0]),n=(0,C.Z)(t,2);return n[0]/n[1]}function I(e){return e.split(/\n|\r\n|\r/).filter((function(e){return!!e})).map((function(e){var t=e.split("\t"),n=(0,A.Z)(t),a=n[0],u=n[2],s=n[3],c=n[4],i=n[5],o=n[7],f=n[8],l=n[9],p=n[10],m=n[11],h=n.slice(12),v=Object.fromEntries(h.map((function(e){var t=e.indexOf(":");return[e.slice(0,t),e.slice(t+3)]})));return{tname:i,tstart:+o,tend:+f,qname:a,qstart:+u,qend:+s,strand:"-"===c?-1:1,extra:(0,r.Z)({numMatches:+l,blockLen:+p,mappingQual:+m},v)}}))}function O(e){for(var t=[],n=e.length-2;n>=0;n-=2){t.push(e[n]);var r=e[n+1];"D"===r?t.push("I"):"I"===r?t.push("D"):t.push(r)}return t}var R=["numMatches","blockLen","cg"],S=y.tr.parseCigar,j=function(e){(0,l.Z)(n,e);var t=(0,p.Z)(n);function n(){var e;(0,o.Z)(this,n);for(var r=arguments.length,a=new Array(r),u=0;u<r;u++)a[u]=arguments[u];return(e=t.call.apply(t,[this].concat(a))).setupP=void 0,e}return(0,f.Z)(n,[{key:"setup",value:function(){var e=(0,i.Z)((0,c.Z)().mark((function e(t){var n=this;return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this.setupP||(this.setupP=this.setupPre(t).catch((function(e){throw n.setupP=void 0,e}))),e.abrupt("return",this.setupP);case 2:case"end":return e.stop()}}),e,this)})));return function(t){return e.apply(this,arguments)}}()},{key:"setupPre",value:function(){var e=(0,i.Z)((0,c.Z)().mark((function e(t){var n,r,a,u,s;return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return n=this.pluginManager,r=(0,v.openLocation)(this.getConf("pafLocation"),n),e.next=4,r.readFile(t);case 4:if(a=e.sent,!(0,N.lq)(a)){e.next=11;break}return e.next=8,(0,b.unzip)(a);case 8:e.t0=e.sent,e.next=12;break;case 11:e.t0=a;case 12:if(!((u=e.t0).length>536870888)){e.next=15;break}throw new Error("Data exceeds maximum string length (512MB)");case 15:return s=new TextDecoder("utf8",{fatal:!0}).decode(u),e.abrupt("return",I(s));case 17:case"end":return e.stop()}}),e,this)})));return function(t){return e.apply(this,arguments)}}()},{key:"hasDataForRefName",value:function(){var e=(0,i.Z)((0,c.Z)().mark((function e(){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",!0);case 1:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}()},{key:"getAssemblyNames",value:function(){var e=this.getConf("assemblyNames");return 0===e.length?[this.getConf("queryAssembly"),this.getConf("targetAssembly")]:e}},{key:"getRefNames",value:function(){var e=(0,i.Z)((0,c.Z)().mark((function e(){var t,n,r,a,i,o,f,l,p,m=arguments;return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r=null===(t=(n=m.length>0&&void 0!==m[0]?m[0]:{}).regions)||void 0===t?void 0:t[0].assemblyName,e.next=4,this.setup(n);case 4:if(a=e.sent,-1===(i=this.getAssemblyNames().indexOf(r))){e.next=11;break}o=new Set,f=(0,s.Z)(a);try{for(f.s();!(l=f.n()).done;)p=l.value,o.add(0===i?p.qname:p.tname)}catch(c){f.e(c)}finally{f.f()}return e.abrupt("return",(0,u.Z)(o));case 11:return console.warn("Unable to do ref renaming on adapter"),e.abrupt("return",[]);case 13:case"end":return e.stop()}}),e,this)})));return function(){return e.apply(this,arguments)}}()},{key:"getFeatures",value:function(e){var t=this,n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return(0,d.ObservableCreate)(function(){var u=(0,i.Z)((0,c.Z)().mark((function u(s){var i,o,f,l,p,m,v,d,b,y,Z,x,k,w,N,A,C,D,I,j,F,L,P,_,B,E;return(0,c.Z)().wrap((function(u){for(;;)switch(u.prev=u.next){case 0:return u.next=2,t.setup(n);case 2:for(i=u.sent,(o=n.config)&&"meanQueryIdentity"===(0,g.readConfObject)(o,"colorBy")&&(i=M(i)),f=t.getAssemblyNames(),l=f.indexOf(e.assemblyName),p=e.start,m=e.end,v=e.refName,d=e.assemblyName,-1===l&&(console.warn("".concat(d," not found in this adapter")),s.complete()),b=0;b<i.length;b++)y=i[b],Z=0,x=0,k="",w="",N=0,A=0,D=f[+!(C=0===l)],0===l?(Z=y.qstart,x=y.qend,k=y.qname,w=y.tname,N=y.tstart,A=y.tend):(Z=y.tstart,x=y.tend,k=y.tname,w=y.qname,N=y.qstart,A=y.qend),I=y.extra,j=y.strand,k===v&&(0,h.qY)(p,m,Z,x)&&(F=I.numMatches,L=void 0===F?0:F,P=I.blockLen,_=void 0===P?1:P,I.cg,B=(0,a.Z)(I,R),E=I.cg,I.cg&&(C&&-1===j?E=O(S(I.cg)).join(""):C&&(c=I.cg,E=c.replaceAll("D","K").replaceAll("I","D").replaceAll("K","I"))),s.next(new q((0,r.Z)((0,r.Z)({uniqueId:b+D,assemblyName:D,start:Z,end:x,type:"match",refName:k,strand:j},B),{},{CIGAR:E,syntenyId:b,identity:L/_,numMatches:L,blockLen:_,mate:{start:N,end:A,refName:w,assemblyName:f[+C]}}))));s.complete();case 11:case"end":return u.stop()}var c}),u)})));return function(e){return u.apply(this,arguments)}}())}},{key:"freeResources",value:function(){}}]),n}(m.BaseFeatureDataAdapter);j.capabilities=["getFeatures","getRefNames"]},44922:function(e,t,n){n.d(t,{$R:function(){return l},SN:function(){return i},lq:function(){return c},pJ:function(){return o}});var r=n(32723),a=n(34795),u=n(96234),s=n(16959);function c(e){return 31===e[0]&&139===e[1]&&8===e[2]}function i(e){return new Map(e.split(/\n|\r\n|\r/).filter((function(e){return!!e||e.startsWith("#")})).map((function(e){var t=e.split("\t"),n=(0,u.Z)(t,6),r=n[0],a=n[1],s=n[2],c=n[3];return[c,{refName:r,start:+a,end:+s,score:+n[4],name:c,strand:"-"===n[5]?-1:1}]})))}function o(e,t){return f.apply(this,arguments)}function f(){return(f=(0,a.Z)((0,r.Z)().mark((function e(t,n){var a;return(0,r.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,t.readFile(n);case 2:if(a=e.sent,e.t0=new TextDecoder("utf8",{fatal:!0}),!c(a)){e.next=10;break}return e.next=7,(0,s.unzip)(a);case 7:e.t1=e.sent,e.next=11;break;case 10:e.t1=a;case 11:return e.t2=e.t1,e.abrupt("return",e.t0.decode.call(e.t0,e.t2));case 13:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function l(e,t){return e.map((function(e,n){return[e,t[n]]}))}}}]);
//# sourceMappingURL=644.2d3d44bb.chunk.js.map