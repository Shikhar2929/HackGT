<img src="AlphaMine Logo.png" style="width:500px;height:600px;">
<hr>

<h3>Problem Statement</h3>
<p> <i>"Data is the new Oil." - Clive Humby </i> <br> Machine Learning has gained traction in recent years. However, training and validating machine learning requires the availability of labeled data at scale. The new demands of data ensure that data collection will always be a consistent struggle.
<br>
<br> 
<strong>
Enter the AlphaMine. Our framework allows users to simply enter keywords and our alpha software will automatically generate a dataset, cleaned and prepared for training. 
  </strong>
  
</p>


<hr>

<h3>Text Mining</h3>
<br>
<p>Text Mining can be extremely useful for Natural Language Processing applications. With easy dataset generation, sophisticated models like GPT-3 will become more accessible to a wider audience.</p>
<ul>
  <li> <strong> Parameters </strong> <ul> 
  <li>Number of Classes</li>
  <li>Number of Samples (Webpages Traversed)</li>
  </ul></li>
  
</ul>
<h3>Image Mining</h3>
<p> AlphaMine also supports Computer Vision dataset generation. 
<ul>
  <li><strong> Parameters </strong> <ul> 
  <li>Number of Classes</li>
  <li>Number of Samples (Images Traversed)</li>
  <li>Size - A Tuple. Optional parameter, default will not resize the images</li> 
  <li>Number of Grayscale. Optional parameter, defaulted to no Grayscale</li> 
  <li>Boundary boxes, generated from yolo model on 80 common classes. Box locations are stored in meta_images.json</li>
  </ul></li>
  
</ul>
<h3>Installation Instructions</h3>
<h3>Command-Line Usage</h3>
Simply follow the installation instructions and then run the following script
<br>
<code>
python3 mine_data.py
</code>
<h3>Library Usage</h3>
