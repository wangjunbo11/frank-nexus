"""Upload an already-built site to an existing Tencent COS bucket.
Domain, bucket website configuration, DNS and HTTPS are managed separately.
Credentials are read from environment only. No bucket creation or deletion.
"""
from pathlib import Path
import os,mimetypes

def main():
    from qcloud_cos import CosConfig,CosS3Client
    required=['COS_REGION','COS_BUCKET','COS_SECRET_ID','COS_SECRET_KEY']
    missing=[k for k in required if not os.environ.get(k)]
    if missing:raise SystemExit('Missing deployment settings: '+', '.join(missing))
    config=CosConfig(Region=os.environ['COS_REGION'],SecretId=os.environ['COS_SECRET_ID'],SecretKey=os.environ['COS_SECRET_KEY'],Token=os.environ.get('COS_SESSION_TOKEN') or None,Scheme='https')
    client=CosS3Client(config);root=Path(__file__).resolve().parents[1]/'dist'
    files=sorted((p for p in root.rglob('*') if p.is_file() and not p.name.startswith('.')),key=lambda p:(p==root/'index.html',p.suffix=='.html',str(p)))
    for path in files:
        content_type=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        if content_type.startswith('text/') or path.suffix in ['.js','.json']:content_type+='; charset=utf-8'
        with path.open('rb') as body:
            client.put_object(Bucket=os.environ['COS_BUCKET'],Key=path.relative_to(root).as_posix(),Body=body,ContentType=content_type,CacheControl='no-cache')
    print('Uploaded',len(files),'site files. Verify the configured custom domain and HTTPS separately.')
if __name__=='__main__':main()
