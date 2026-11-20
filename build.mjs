import {mkdir,copyFile,cp,rm} from 'node:fs/promises';
const files=['index.html','landing.css','landing.js','service-config.js','brand.svg'];
await rm('dist',{recursive:true,force:true});await mkdir('dist',{recursive:true});
for(const file of files)await copyFile(file,'dist/'+file);
console.log('Public landing built in dist/. Legacy single-company app is not published.');
