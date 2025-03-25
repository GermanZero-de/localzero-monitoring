'use client';

import React, { useState } from 'react';
import { Modal, CloseButton } from 'react-bootstrap';
import Markdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm'

interface ImageModalProps {
  src: string;
  alt?: string;
  title?: string;
  className?: string;
  style?: React.CSSProperties;
  modalTitle?: string;
  caption?: string;
  license?: string;
  source?: string;
}

const ImageModal: React.FC<ImageModalProps> = ({
  src,
  alt = '',
  title = '',
  className = '',
  license = '',
  caption = '',
  source = '',
  style = {},
}) => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      {/* Clickable image */}
      <figure>
        <img className={`d-block border ${className}`}
            title={title}
            alt={title}
            src={ src }
            onClick={handleShow}

            />
        <figcaption>
        <Markdown rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]} className="mdContent">{caption}</Markdown>
            <span className="text-muted">Quelle: { source } - Lizenz: { license }</span>
        </figcaption>
     </figure>

      {/* Modal for large image */}
      <Modal show={show} onHide={handleClose} centered fullscreen>
        <Modal.Body className='m-auto'>
        <CloseButton onClick={handleClose} style={{position:"absolute",right:0, top:10}}/>
        <figure className='h-100 m-auto text-center'>
            <img className={`m-auto d-block border ${className}`}
                title={title}
                alt={title}
                src={ src }
                onClick={handleClose}
                style={{maxHeight: "90%"}}
                />
            <figcaption>
            <Markdown rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]} className="mdContent">{caption}</Markdown>
                <span className="text-muted">Quelle: { source } - Lizenz: { license }</span>
            </figcaption>
        </figure>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default ImageModal;
