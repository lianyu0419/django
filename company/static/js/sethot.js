 //锟斤拷锟斤拷锟秸诧拷 function AddFavorite(sURL, sTitle) { sURL = encodeURI(sURL); try{ window.external.addFavorite(sURL, sTitle); }catch(e) { try{ window.sidebar.addPanel(sTitle, sURL, ""); }catch (e) { alert("锟斤拷锟斤拷锟秸诧拷失锟杰ｏ拷锟斤拷使锟斤拷Ctrl+D锟斤拷锟斤拷锟斤拷锟斤拷,锟斤拷锟街讹拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷."); } } } //锟斤拷为锟斤拷页 function SetHome(url){ if (document.all) { document.body.style.behavior='url(#default#homepage)'; document.body.setHomePage(url); }else{ alert("锟斤拷锟斤拷,锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟街э拷锟斤拷远锟斤拷锟斤拷锟揭筹拷锟轿拷锟揭筹拷锟斤拷锟�,锟斤拷锟斤拷锟街讹拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷酶锟揭筹拷锟轿拷锟揭�!"); } } 