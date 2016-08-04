def uniform_random(sample_size) :
    pass

def gaussian(sample_size) :
    pass

pdf_types = { 'uniform random': uniform_random,
              'gaussian': gaussian
                  }

def create_pdf(sample_size=None, pdf_type=None) :
    return pdf_types[pdf_type](sample_size) 

